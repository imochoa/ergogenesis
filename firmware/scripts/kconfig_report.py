#!/usr/bin/env python3
"""Generate a self-contained HTML report for a ZMK build's Kconfig.

Run inside the firmware devcontainer after a build:

    python3 scripts/kconfig_report.py .build/nice_nano/ergogenesis_left \
      .build/nice_nano/ergogenesis_left/zephyr/kconfig-report.html

The script uses Zephyr's vendored Kconfiglib, so it needs no network access or
additional Python packages.
"""

from __future__ import annotations

import argparse
import html
import os
import shlex
import sys
from pathlib import Path


def configured_symbols(config: Path) -> list[str]:
    """Return CONFIG symbol names in their generated .config order."""
    names: list[str] = []
    for line in config.read_text(encoding="utf-8").splitlines():
        if line.startswith("CONFIG_"):
            names.append(line.partition("=")[0][len("CONFIG_") :])
        elif line.startswith("# CONFIG_") and line.endswith(" is not set"):
            names.append(line[len("# CONFIG_") : -len(" is not set")])
    return names


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def build_environment(build_dir: Path) -> dict[str, str]:
    """Reuse the environment CMake generated for Zephyr's Kconfig tools."""
    ninja = build_dir / "build.ninja"
    for line in ninja.read_text(encoding="utf-8").splitlines():
        if "menuconfig.py" not in line or "cmake -E env " not in line:
            continue
        command = line.split("cmake -E env ", 1)[1]
        words = shlex.split(command)
        environment: dict[str, str] = {}
        for word in words:
            if word == "/usr/bin/python3":
                return environment
            key, separator, value = word.partition("=")
            if separator:
                environment[key] = value
    raise RuntimeError(f"could not find Kconfig environment in {ninja}")


def symbol_row(kconfiglib, kconf, name: str) -> str:
    symbol = kconf.syms.get(name)
    if symbol is None:
        return (
            f"<tr><td><code>CONFIG_{esc(name)}</code></td><td>unknown</td>"
            "<td colspan=5>Not found in the parsed Kconfig tree.</td></tr>"
        )

    nodes = symbol.nodes
    prompt = next((node.prompt[0] for node in nodes if node.prompt), "")
    help_text = next((node.help for node in nodes if node.help), "")
    locations = "<br>".join(
        esc(f"{node.filename}:{node.linenr}") for node in nodes
    )
    dependencies = kconfiglib.expr_str(symbol.direct_dep)
    defaults = "; ".join(
        f"{kconfiglib.expr_str(value)} if {kconfiglib.expr_str(condition)}"
        for value, condition in symbol.defaults
    )
    value = symbol.str_value
    enabled = "yes" if value in {"y", "m"} else "no"

    return "".join(
        [
            "<tr>",
            f'<td><code>CONFIG_{esc(name)}</code></td>',
            f'<td class="value" data-enabled="{enabled}">{esc(value)}</td>',
            f"<td>{esc(kconfiglib.TYPE_TO_STR[symbol.type])}</td>",
            f"<td>{esc(prompt)}</td>",
            f"<td>{esc(help_text)}</td>",
            f"<td><code>{esc(dependencies)}</code></td>",
            f"<td><code>{esc(defaults)}</code></td>",
            f"<td><code>{locations}</code></td>",
            "</tr>",
        ]
    )


def report(title: str, rows: list[str]) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)} — Kconfig report</title>
  <style>
    :root {{ color-scheme: light dark; font-family: system-ui, sans-serif; }}
    body {{ margin: 1.5rem; }}
    input {{ font: inherit; margin: .5rem 0 1rem; max-width: 42rem; padding: .5rem; width: 100%; }}
    .summary {{ color: #666; }}
    .table-wrap {{ overflow-x: auto; }}
    table {{ border-collapse: collapse; font-size: .85rem; width: 100%; }}
    th, td {{ border: 1px solid #8886; padding: .5rem; text-align: left; vertical-align: top; }}
    th {{ position: sticky; top: 0; background: Canvas; }}
    code {{ font-family: ui-monospace, monospace; white-space: pre-wrap; }}
    td:nth-child(5) {{ min-width: 20rem; white-space: pre-wrap; }}
    .value[data-enabled="yes"] {{ color: #16803c; font-weight: bold; }}
  </style>
</head>
<body>
  <h1>{esc(title)} — Kconfig report</h1>
  <p class="summary">Generated from the effective <code>.config</code>. Search matches symbol names, values, prompts, help, dependencies, defaults, and definition locations.</p>
  <label>Search <input id="search" type="search" autofocus placeholder="e.g. ZMK_BLE, bluetooth, GPIO"></label>
  <p id="count"></p>
  <div class="table-wrap">
    <table>
      <thead><tr><th>Symbol</th><th>Value</th><th>Type</th><th>Prompt</th><th>Help</th><th>Depends on</th><th>Defaults</th><th>Defined at</th></tr></thead>
      <tbody>{''.join(rows)}</tbody>
    </table>
  </div>
  <script>
    const rows = [...document.querySelectorAll('tbody tr')];
    const input = document.querySelector('#search');
    const count = document.querySelector('#count');
    function filter() {{
      const query = input.value.toLowerCase();
      let shown = 0;
      for (const row of rows) {{
        const match = row.textContent.toLowerCase().includes(query);
        row.hidden = !match;
        shown += match;
      }}
      count.textContent = `${{shown}} of ${{rows.length}} symbols shown`;
    }}
    input.addEventListener('input', filter);
    filter();
  </script>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("build_dir", type=Path, help="Build directory for one target")
    parser.add_argument("output", type=Path, help="HTML report path")
    args = parser.parse_args()

    firmware = Path(__file__).resolve().parents[1]
    build_dir = args.build_dir.resolve()
    config = build_dir / "zephyr" / ".config"
    if not config.is_file():
        parser.error(f"generated config not found: {config}")

    zephyr_base = firmware / "zephyr"
    sys.path.insert(0, str(zephyr_base / "scripts" / "kconfig"))
    import kconfiglib  # Zephyr's vendored copy

    os.environ.update(build_environment(build_dir))
    os.environ.update(
        {
            # ZMK's Kconfig sources Zephyr paths with `source`, while its own
            # paths use `rsource`, so srctree must be the Zephyr source root.
            "srctree": str(zephyr_base),
            "ZEPHYR_BASE": str(zephyr_base),
            "ZMK_CONFIG": str(firmware / "config"),
            "KCONFIG_BINARY_DIR": str(build_dir / "Kconfig"),
            "KCONFIG_CONFIG": str(config),
        }
    )
    kconf = kconfiglib.Kconfig(str(firmware / "zmk" / "app" / "Kconfig"), warn=False)
    kconf.load_config(str(config))
    rows = [
        symbol_row(kconfiglib, kconf, name) for name in configured_symbols(config)
    ]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report(build_dir.name, rows), encoding="utf-8")
    print(f"Wrote {args.output} ({len(rows)} configured symbols)")


if __name__ == "__main__":
    main()
