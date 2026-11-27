#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "typer>=0.12",
#     "rich>=13",
#     "sh>=2.0",
#     "pyyaml>=6",
# ]
# ///
"""Generate an OverKeys config from the ergogenesis ZMK keymap.

Labels come from keymap-drawer's parse of firmware/config/ergogenesis.keymap,
key positions from the zmk,physical-layout node in ergogenesis.dtsi.

    ./convert.py                      # no args -> prints command list
    ./convert.py convert              # writes output/overkeys_config.json
    ./convert.py install              # dry run: shows where the config would go
    ./convert.py install --no-dry-run
"""

from __future__ import annotations

import json
import logging
import os
import re
import shutil
from pathlib import Path

import sh
import typer
import yaml
from rich.logging import RichHandler

log = logging.getLogger("overkeys")
app = typer.Typer(add_completion=False, help=__doc__, no_args_is_help=True)

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
KEYMAP = REPO / "firmware/config/ergogenesis.keymap"
DTSI = REPO / "firmware/config/boards/shields/ergogenesis/ergogenesis.dtsi"
DRAW_CONFIG = REPO / "firmware/draw/config.yaml"
OUTPUT = HERE / "output/overkeys_config.json"
INSTALLED = (
    Path.home() / "Library/Application Support/com.example.overkeys/overkeys_config.json"
)

# Layer display-name -> key the firmware holds while that layer is active.
# Keep in sync with the OVK_* defines in firmware/config/ergogenesis.keymap.
# macOS only reports F1-F20, so F21-F24 cannot be triggers.
TRIGGERS = {"Symbols": "F20"}

NAME_PREFIX = "Ergogenesis "
COLS = 5  # main columns per hand
ROWS = 3
THUMBS = 3  # thumb keys per hand
KEYS = 2 * (COLS * ROWS + THUMBS)

# keymap-drawer legend -> the key name OverKeys reports on macOS, so the
# overlay highlights the key when it is pressed. Unlisted legends pass through.
OVERKEYS_NAME = {
    "Bspc": "Backspace",
    "BKSP": "Backspace",
    "Del": "Delete",
    "Esc": "Escape",
    "ENTER": "Enter",
    "Spc": " ",
    "←": "Left",
    "→": "Right",
    "↑": "Up",
    "↓": "Down",
    "PgUp": "PageUp",
    "PgDn": "PageDown",
    "Ins": "Insert",
    "Gui": "Cmd",
    "Ctrl": "LControl",
    "Alt": "LAlt",
    "Shift": "LShift",
    "LSHIFT": "LShift",
    "RSHIFT": "RShift",
}


def _setup_logging(log_level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format="%(message)s",
        datefmt="[%H:%M:%S]",
        handlers=[
            RichHandler(rich_tracebacks=True, show_path=False, markup=False, keywords=[])
        ],
    )
    logging.getLogger("sh").setLevel(logging.WARNING)


def _fail(message: str, *args: object) -> typer.Exit:
    log.error(message, *args)
    return typer.Exit(code=1)


def parse_keymap() -> dict:
    """Run keymap-drawer on the ZMK keymap and return its parsed YAML."""
    # The nix dev shell's PYTHONPATH breaks uvx's interpreter (see draw.just).
    env = {k: v for k, v in os.environ.items() if k not in ("PYTHONPATH", "PYTHONHOME")}
    try:
        out = sh.uvx(
            "--from", "keymap-drawer", "keymap",
            "-c", str(DRAW_CONFIG), "parse", "-z", str(KEYMAP),
            _tty_out=False, _cwd=str(REPO), _env=env,
        )  # fmt: skip
    except sh.CommandNotFound:
        raise _fail("uvx not found on PATH; install uv first.")
    except sh.ErrorReturnCode as exc:
        stderr = (exc.stderr or b"").decode(errors="replace").strip() or "(no stderr)"
        raise _fail("keymap-drawer failed: %s", stderr)
    return yaml.safe_load(str(out))


def physical_layout() -> dict:
    """Read key positions (1/100 key units) from the zmk,physical-layout node."""
    attrs = re.findall(
        r"<&key_physical_attrs\s+(\d+)\s+(\d+)\s+(-?\d+)\s+(-?\d+)\s+\(?(-?\d+)\)?",
        DTSI.read_text(encoding="utf-8"),
    )
    if len(attrs) != KEYS:
        raise _fail("expected %d keys in %s, found %d", KEYS, DTSI.name, len(attrs))
    pos = [(int(x) / 100, int(y) / 100, int(rot) / 100) for _, _, x, y, rot in attrs]

    hands: dict[str, dict[str, list]] = {
        "leftHand": {"keys": [], "thumbKeys": []},
        "rightHand": {"keys": [], "thumbKeys": []},
    }
    main = 2 * COLS * ROWS
    for i, (x, y, _) in enumerate(pos[:main]):
        row, col = divmod(i, 2 * COLS)
        hand = "leftHand" if col < COLS else "rightHand"
        hands[hand]["keys"].append({"row": row, "col": col % COLS, "x": x, "y": y})
    for i, (x, y, rot) in enumerate(pos[main:]):
        hand, side = ("leftHand", "L") if i < THUMBS else ("rightHand", "R")
        hands[hand]["thumbKeys"].append(
            {"id": f"{side}_T{i % THUMBS}", "x": x, "y": y, "rotate": rot}
        )
    return {"unit": "keyUnits", "keySize": 46, "keyPadding": 3, **hands}


def label(key: object, base: object | None) -> str:
    """Resolve one keymap-drawer key to an OverKeys label.

    Transparent and held keys show the base-layer key; hold-taps show the tap.
    """
    if isinstance(key, dict):
        if key.get("type") in ("trans", "held") and not key.get("t"):
            return label(base, None) if base is not None else ""
        key = key.get("t") or key.get("h") or ""
    text = "" if key is None else str(key)
    return OVERKEYS_NAME.get(text, text)


def split_layer(labels: list[str]) -> dict:
    """Split a flat 36-key layer into OverKeys' leftHand/rightHand rows."""
    main = 2 * COLS * ROWS
    rows = [labels[i : i + 2 * COLS] for i in range(0, main, 2 * COLS)]
    return {
        "leftHand": {
            "mainRows": [row[:COLS] for row in rows],
            "thumbRows": [labels[main : main + THUMBS]],
        },
        "rightHand": {
            "mainRows": [row[COLS:] for row in rows],
            "thumbRows": [labels[main + THUMBS :]],
        },
    }


def build_config(parsed: dict) -> dict:
    layers: dict[str, list] = parsed["layers"]
    base_name, base = next(iter(layers.items()))
    for name in TRIGGERS:
        if name not in layers:
            raise _fail("TRIGGERS names layer %r, keymap has %s", name, list(layers))

    user_layouts = []
    for name, keys in layers.items():
        if len(keys) != KEYS:
            raise _fail("layer %r has %d keys, expected %d", name, len(keys), KEYS)
        is_base = name == base_name
        labels = [label(k, None if is_base else b) for k, b in zip(keys, base)]
        layout = {"name": NAME_PREFIX + name, **split_layer(labels)}
        if name in TRIGGERS:
            layout |= {"trigger": TRIGGERS[name], "type": "held"}
        user_layouts.append(layout)
        log.info("layer %-10s trigger: %s", name, TRIGGERS.get(name, "-"))

    return {
        "defaultUserLayout": NAME_PREFIX + base_name,
        "physicalLayout": physical_layout(),
        "ignoredKeys": sorted(set(TRIGGERS.values())),
        "userLayouts": user_layouts,
    }


@app.command()
def convert(
    output: Path = typer.Option(OUTPUT, "--output", "-o", help="Config file to write."),
    log_level: str = typer.Option("INFO", "--log-level", help="Python logging level."),
):
    """Parse the ZMK keymap and write the OverKeys config."""
    _setup_logging(log_level)
    config = build_config(parse_keymap())
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    log.info("wrote %s (%d layouts)", output, len(config["userLayouts"]))


@app.command()
def install(
    source: Path = typer.Option(OUTPUT, "--source", "-s", help="Generated config."),
    dest: Path = typer.Option(INSTALLED, "--dest", help="OverKeys config location."),
    dry_run: bool = typer.Option(
        True,
        "--dry-run/--no-dry-run",
        help="Dry run logs what WOULD happen without doing it. Default: on.",
    ),
    log_level: str = typer.Option("INFO", "--log-level", help="Python logging level."),
):
    """Copy the generated config to OverKeys, backing up the existing one."""
    _setup_logging(log_level)
    if not source.exists():
        raise _fail("%s not found; run `convert` first.", source)
    backup = dest.with_suffix(".json.bak")
    if dry_run:
        if dest.exists():
            log.info("WOULD back up %s -> %s", dest, backup.name)
        log.info("WOULD copy %s -> %s", source, dest)
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        shutil.copy2(dest, backup)
        log.info("backed up existing config to %s", backup)
    shutil.copy2(source, dest)
    log.info("installed %s; use 'Reload config' in the OverKeys tray menu", dest)


if __name__ == "__main__":
    app()
