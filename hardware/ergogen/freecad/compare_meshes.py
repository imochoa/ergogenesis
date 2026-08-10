#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "typer>=0.12",
#     "rich>=13",
#     "numpy>=1.26",
#     "scipy>=1.11",
#     "rtree>=1.2.0",
#     "trimesh>=4.4",
# ]
# ///
"""Compare two meshes (e.g., JSCAD vs FreeCAD STL) by volume, area, and an
approximate bidirectional Hausdorff distance.

Examples:
  ./compare_meshes.py compare A.stl B.stl
  ./compare_meshes.py stats A.stl
"""

from __future__ import annotations

import logging
import math
from pathlib import Path

import numpy as np
import typer
from rich.logging import RichHandler
import trimesh

log = logging.getLogger("compare_meshes")
app = typer.Typer(add_completion=False, help=__doc__, no_args_is_help=True)


def _setup_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(message)s",
        datefmt="[%H:%M:%S]",
        handlers=[RichHandler(rich_tracebacks=True, show_path=False, markup=False, keywords=[])],
    )


def _directed_hausdorff(A: trimesh.Trimesh, B: trimesh.Trimesh, samples: int) -> float:
    pts, _ = trimesh.sample.sample_surface_even(A, samples)
    pq = trimesh.proximity.ProximityQuery(B)
    d = pq.signed_distance(pts)
    d = np.nan_to_num(d, nan=0.0)
    return float(np.max(np.abs(d)))


@app.command()
def stats(
    mesh: Path = typer.Argument(..., help="Path to STL/PLY/OBJ mesh"),
    log_level: str = typer.Option("INFO", "--log-level", help="Python logging level"),
):
    """Print individual mesh stats (volume, area)."""
    _setup_logging(log_level)
    m = trimesh.load(mesh, force="mesh", process=True)
    if not m.is_volume:
        log.warning("mesh %s is not watertight; volume may be inaccurate", mesh)
    log.info("volume: %.6f mm^3", m.volume)
    log.info("area:   %.6f mm^2", m.area)


@app.command()
def compare(
    a: Path = typer.Argument(..., help="Mesh A (e.g., JSCAD STL)"),
    b: Path = typer.Argument(..., help="Mesh B (e.g., FreeCAD STL)"),
    vol_rel: float = typer.Option(1e-3, "--vol-rel", help="Max relative volume diff (0.001 = 0.1%)"),
    hausdorff: float = typer.Option(0.05, "--hausdorff", help="Max approx bidirectional Hausdorff distance (mm)"),
    samples: int = typer.Option(5000, "--samples", help="Samples per direction for Hausdorff"),
    log_level: str = typer.Option("INFO", "--log-level", help="Python logging level"),
):
    """Compare two meshes and exit 0 if within tolerances."""
    _setup_logging(log_level)
    A = trimesh.load(a, force="mesh", process=True)
    B = trimesh.load(b, force="mesh", process=True)

    if not (A.is_volume and B.is_volume):
        log.warning("one or both meshes are not watertight; volume may be inaccurate")

    vol_a = float(A.volume)
    vol_b = float(B.volume)
    area_a = float(A.area)
    area_b = float(B.area)

    vol_abs = abs(vol_a - vol_b)
    vol_rel_calc = vol_abs / max(vol_a, vol_b, 1e-9)
    area_abs = abs(area_a - area_b)

    h_ab = _directed_hausdorff(A, B, samples)
    h_ba = _directed_hausdorff(B, A, samples)
    hmax = max(h_ab, h_ba)

    log.info("A: %s", a)
    log.info("B: %s", b)
    log.info("Volume A/B: %.6f / %.6f mm^3 -> |Δ|=%.6f (%.4f%%)", vol_a, vol_b, vol_abs, vol_rel_calc * 100)
    log.info("Area   A/B: %.6f / %.6f mm^2 -> |Δ|=%.6f", area_a, area_b, area_abs)
    log.info("Approx Hausdorff (A→B, B→A): %.4f mm, %.4f mm -> max=%.4f mm", h_ab, h_ba, hmax)

    ok = (vol_rel_calc <= vol_rel) and (hmax <= hausdorff)
    if ok:
        log.info("Result: MATCH")
        raise typer.Exit(code=0)
    else:
        log.error("Result: DIFFER (vol_rel=%.6f, hausdorff=%.4f mm)", vol_rel_calc, hmax)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
