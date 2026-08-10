#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "typer>=0.12",
#     "rich>=13",
#     "sh>=2.0",
#     "numpy>=1.26",
#     "trimesh>=4.4",
# ]
# ///
"""Build FreeCAD STEP/STL from Ergogen DXFs and compare to JSCAD STLs.
Iteratively refine the FreeCAD mesh (linear deflection) until comparison passes.

Examples:
  ./iterate_compare.py run                       # all pieces
  ./iterate_compare.py run --pieces switch       # just the switch plate
  ./iterate_compare.py find-freecad              # print detected FreeCADCmd path
"""

from __future__ import annotations

import logging
import os
import re
from pathlib import Path
from typing import Iterable

import numpy as np
import sh
import trimesh
import typer
from rich.logging import RichHandler

THIS = Path(__file__).resolve()
ERGOGEN = THIS.parents[1]
OUTLINES = ERGOGEN / "output" / "outlines"
CASES = ERGOGEN / "output" / "cases"
CONFIG = ERGOGEN / "config.yaml"

PIECES = ["switch", "bottom", "case"]

log = logging.getLogger("iterate_compare")
app = typer.Typer(add_completion=False, help=__doc__, no_args_is_help=True)


def _setup_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(message)s",
        datefmt="[%H:%M:%S]",
        handlers=[RichHandler(rich_tracebacks=True, show_path=False, markup=False, keywords=[])],
    )
    logging.getLogger("sh").setLevel(logging.WARNING)


def _exists_x(p: Path) -> bool:
    try:
        return p.exists() and os.access(p, os.X_OK)
    except Exception:
        return False


def _glob_candidates(pattern: str) -> Iterable[Path]:
    return sorted((Path("/") / pattern).glob("**/*"))


def find_freecad_cmd() -> Path | None:
    # 1) env var
    env = os.environ.get("FREECAD_CMD")
    if env:
        p = Path(env)
        if _exists_x(p):
            return p
    # 2) PATH (try both capitalized and lowercase)
    try:
        found = str(sh.bash("-lc", "command -v FreeCADCmd freecadcmd 2>/dev/null | head -n1 || true", _tty_out=False)).strip()
        if found:
            p = Path(found)
            if _exists_x(p):
                return p
    except sh.ErrorReturnCode:
        pass
    # 3) common brew/cask locations (macOS)
    candidates = [
        Path("/Applications/FreeCAD.app/Contents/MacOS/FreeCADCmd"),
        Path("/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd"),
        Path("/opt/homebrew/bin/FreeCADCmd"),
        Path("/opt/homebrew/bin/freecadcmd"),
        Path("/usr/local/bin/FreeCADCmd"),
        Path("/usr/local/bin/freecadcmd"),
    ]
    # Caskroom installs with versioned subdirs; pick the newest if present
    for base in (Path("/opt/homebrew/Caskroom/freecad"), Path("/usr/local/Caskroom/freecad")):
        if base.exists():
            for sub in sorted(base.iterdir(), reverse=True):
                for rel in (
                    Path("FreeCAD.app/Contents/MacOS/FreeCADCmd"),
                    Path("FreeCAD.app/Contents/Resources/bin/freecadcmd"),
                ):
                    cand = sub / rel
                    if _exists_x(cand):
                        candidates.append(cand)
                        break
    for c in candidates:
        if _exists_x(c):
            return c
    return None


def _run(cmd, *args: str) -> str:
    try:
        return str(cmd(*args, _tty_out=False))
    except sh.CommandNotFound:
        log.error("command not found: %s", getattr(cmd, "_path", cmd))
        raise typer.Exit(code=1)
    except sh.ErrorReturnCode as exc:
        err = (exc.stderr or b"").decode(errors="replace").strip()
        log.error("command failed: %s", err or "(no stderr)")
        raise typer.Exit(code=1)


def read_units() -> dict[str, float]:
    text = CONFIG.read_text()
    def grab(key: str, default: float) -> float:
        m = re.search(rf"^\s*{key}:\s*([0-9.]+)\s*$", text, flags=re.M)
        return float(m.group(1)) if m else default
    return {
        "plate_thickness": grab("plate_thickness", 1.6),
        "bottom_plate_thickness": grab("bottom_plate_thickness", 2.0),
        "standoff_height": grab("standoff_height", 2.0),
        "wall_height": grab("wall_height", 5.0),
    }


def ensure_ergogen_outputs() -> None:
    if not OUTLINES.exists():
        log.info("running: just ergogen-build")
        _run(sh.just, "ergogen-build")
    log.info("running: just ergogen-stl-from-jscad")
    _run(sh.just, "ergogen-stl-from-jscad")


def freecad_extrude(freecad_cmd: Path, dxf_name: str, height: float, step_name: str, stl_name: str, defl: float) -> None:
    dxf = OUTLINES / dxf_name
    step = CASES / step_name
    stl = CASES / stl_name
    log.info("FreeCAD extrude: %s -> %s (h=%.3f, defl=%.4f)", dxf.name, stl.name, height, defl)
    env = {
        "DXF_PATH": str(dxf),
        "HEIGHT_MM": str(height),
        "OUT_STEP": str(step),
        "OUT_STL": str(stl),
        "LINEAR_DEFL": str(defl),
    }
    cmd = sh.Command(str(freecad_cmd))
    try:
        _ = cmd(str(ERGOGEN / "freecad" / "entry_extrude_env.py"), _tty_out=False, _env=env)
    except sh.ErrorReturnCode as exc:
        err = (exc.stderr or b"").decode(errors="replace").strip()
        log.error("FreeCAD extrude failed: %s", err or "(no stderr)")
        raise


def freecad_build_case(freecad_cmd: Path, units: dict[str, float], defl: float) -> None:
    log.info("FreeCAD build case (defl=%.4f)")
    env = {
        "DXF_DIR": str(OUTLINES),
        "BOTTOM_TH": str(units["bottom_plate_thickness"]),
        "STANDOFF_H": str(units["standoff_height"]),
        "WALL_H": str(units["wall_height"]),
        "OUT_STEP": str(CASES / "case_freecad.step"),
        "OUT_STL": str(CASES / "case_freecad.stl"),
        "LINEAR_DEFL": str(defl),
    }
    cmd = sh.Command(str(freecad_cmd))
    try:
        _ = cmd(str(ERGOGEN / "freecad" / "entry_build_case_env.py"), _tty_out=False, _env=env)
    except sh.ErrorReturnCode as exc:
        err = (exc.stderr or b"").decode(errors="replace").strip()
        log.error("FreeCAD case failed: %s", err or "(no stderr)")
        raise


def compare_meshes(jscad_stl: Path, freecad_stl: Path, vol_rel: float, hausdorff: float, samples: int) -> bool:
    A = trimesh.load(jscad_stl, force="mesh", process=True)
    B = trimesh.load(freecad_stl, force="mesh", process=True)
    if not (A.is_volume and B.is_volume):
        log.warning("one or both meshes are not watertight; volume may be inaccurate")
    vol_a = float(A.volume)
    vol_b = float(B.volume)
    area_a = float(A.area)
    area_b = float(B.area)
    vol_abs = abs(vol_a - vol_b)
    vol_rel_calc = vol_abs / max(vol_a, vol_b, 1e-9)
    area_abs = abs(area_a - area_b)
    # approx Hausdorff
    def dh(X, Y):
        pts, _ = trimesh.sample.sample_surface_even(X, samples)
        pq = trimesh.proximity.ProximityQuery(Y)
        d = pq.signed_distance(pts)
        d = np.nan_to_num(d, nan=0.0)
        return float(np.max(np.abs(d)))
    h_ab = dh(A, B)
    h_ba = dh(B, A)
    hmax = max(h_ab, h_ba)

    log.info("Volume A/B: %.6f / %.6f mm^3 -> |Δ|=%.6f (%.4f%%)", vol_a, vol_b, vol_abs, vol_rel_calc * 100)
    log.info("Area   A/B: %.6f / %.6f mm^2 -> |Δ|=%.6f", area_a, area_b, area_abs)
    log.info("Approx Hausdorff (A→B, B→A): %.4f, %.4f -> max=%.4f mm", h_ab, h_ba, hmax)

    ok = (vol_rel_calc <= vol_rel) and (hmax <= hausdorff)
    return ok


@app.command()
def find_freecad(
    log_level: str = typer.Option("INFO", "--log-level", help="Python logging level"),
):
    """Detect FreeCADCmd installed via Homebrew (or common locations) and print its path."""
    _setup_logging(log_level)
    p = find_freecad_cmd()
    if not p:
        log.error("FreeCADCmd not found. Set FREECAD_CMD or install the FreeCAD app via Homebrew.")
        raise typer.Exit(code=1)
    log.info("FreeCADCmd: %s", p)


@app.command()
def run(
    pieces: str = typer.Option("all", "--pieces", case_sensitive=False, help="Which piece(s): all|switch|bottom|case"),
    vol_rel: float = typer.Option(1e-3, "--vol-rel", help="Max relative volume diff (0.001 = 0.1%)"),
    hausdorff: float = typer.Option(0.05, "--hausdorff", help="Max approx Hausdorff distance (mm)"),
    samples: int = typer.Option(5000, "--samples", help="Samples per direction for Hausdorff"),
    defl_start: float = typer.Option(0.1, "--defl-start", help="Initial FreeCAD mesher linear deflection (mm)"),
    defl_min: float = typer.Option(0.01, "--defl-min", help="Minimum linear deflection (mm)"),
    log_level: str = typer.Option("INFO", "--log-level", help="Python logging level"),
):
    """Build FreeCAD STEP/STL and compare to JSCAD STLs, iterating until match."""
    _setup_logging(log_level)

    fc = find_freecad_cmd()
    if not fc:
        log.error("FreeCADCmd not found. Try: brew install --cask freecad")
        raise typer.Exit(code=1)
    else:
        log.info("Using FreeCADCmd: %s", fc)

    units = read_units()
    ensure_ergogen_outputs()

    todo = PIECES if pieces.lower() == "all" else [pieces.lower()]
    for t in todo:
        if t not in PIECES:
            log.error("unknown piece '%s' (choose from all|%s)", t, ",".join(PIECES))
            raise typer.Exit(code=2)

    overall_ok = True

    for piece in todo:
        defl = defl_start
        log.info("=== %s: target vol_rel <= %.6f, hausdorff <= %.3f mm ===", piece, vol_rel, hausdorff)
        while True:
            if piece == "switch":
                freecad_extrude(fc, "switch_plate_ol.dxf", units["plate_thickness"],
                                "switch_plate_freecad.step", "switch_plate_freecad.stl", defl)
                ok = compare_meshes(CASES / "switch_plate.stl", CASES / "switch_plate_freecad.stl", vol_rel, hausdorff, samples)
            elif piece == "bottom":
                freecad_extrude(fc, "bottom_plate_ol.dxf", units["bottom_plate_thickness"],
                                "bottom_plate_freecad.step", "bottom_plate_freecad.stl", defl)
                ok = compare_meshes(CASES / "bottom_plate.stl", CASES / "bottom_plate_freecad.stl", vol_rel, hausdorff, samples)
            else:
                freecad_build_case(fc, units, defl)
                ok = compare_meshes(CASES / "case.stl", CASES / "case_freecad.stl", vol_rel, hausdorff, samples)

            if ok:
                log.info("%s: MATCH at deflection=%.5f", piece, defl)
                break
            else:
                if defl <= defl_min + 1e-9:
                    log.error("%s: FAILED to match within deflection >= %.5f", piece, defl_min)
                    overall_ok = False
                    break
                defl *= 0.5
                if defl < defl_min:
                    defl = defl_min
                log.info("%s: refining mesh, new deflection=%.5f", piece, defl)

    if not overall_ok:
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
