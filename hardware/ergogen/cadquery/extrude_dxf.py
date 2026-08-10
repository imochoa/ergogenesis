#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "cadquery>=2.4",
#     "typer>=0.12",
#     "rich>=13",
# ]
# ///
"""Extrude a DXF profile into a solid and export STEP/STL using CadQuery.

Examples:
  ./extrude_dxf.py run --dxf output/outlines/switch_plate_ol.dxf --height 1.6 \
      --out-step output/cases/switch_plate_cq.step --out-stl output/cases/switch_plate_cq.stl
"""

from __future__ import annotations

import logging
from pathlib import Path

import cadquery as cq
from cadquery import exporters, importers
import typer
from rich.logging import RichHandler

log = logging.getLogger("cq-extrude")
app = typer.Typer(add_completion=False, help=__doc__, no_args_is_help=True)


def _setup_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(message)s",
        datefmt="[%H:%M:%S]",
        handlers=[RichHandler(rich_tracebacks=True, show_path=False, markup=False, keywords=[])],
    )


def _load_dxf_wires(path: Path) -> list[cq.Wire]:
    """Load a DXF into CadQuery wires.

    CadQuery's importers.importDXF returns a Workplane; use .wires().vals().
    """
    wp = importers.importDXF(str(path))
    try:
        wires_wp = wp.wires()
        wires = [w for w in wires_wp.vals() if isinstance(w, cq.Wire) and w.Closed()]
    except Exception as e:
        raise RuntimeError(f"Failed to read wires from DXF {path}: {e}")
    if not wires:
        raise RuntimeError(f"No closed wires found in {path}")
    return wires


def _make_solid(wires: list[cq.Wire], height: float) -> cq.Compound:
    # Create faces from wires, pick largest as base, cut others as holes, extrude
    faces = []
    for w in wires:
        try:
            f = cq.Face.makeFromWires(w)
            faces.append(f)
        except Exception:
            pass
    if not faces:
        raise RuntimeError("No faces could be created from wires")
    faces.sort(key=lambda f: f.Area(), reverse=True)  # type: ignore[attr-defined]
    base = faces[0]
    solid = cq.Workplane("XY").add(base).extrude(height)
    for hf in faces[1:]:
        try:
            hole = cq.Workplane("XY").add(hf).extrude(height)
            solid = solid.cut(hole)
        except Exception:
            pass
    return solid


@app.command()
def run(
    dxf: Path = typer.Option(..., "--dxf", help="Path to DXF outline"),
    height: float = typer.Option(..., "--height", help="Extrude height (mm)"),
    out_step: Path = typer.Option(..., "--out-step", help="Output STEP path"),
    out_stl: Path = typer.Option(None, "--out-stl", help="Optional output STL path"),
    log_level: str = typer.Option("INFO", "--log-level", help="Python logging level"),
):
    _setup_logging(log_level)
    wires = _load_dxf_wires(dxf)
    log.info("loaded %d wires", len(wires))
    solid = _make_solid(wires, height)
    out_step.parent.mkdir(parents=True, exist_ok=True)
    exporters.export(solid, str(out_step))
    log.info("wrote STEP: %s", out_step)
    if out_stl:
        exporters.export(solid, str(out_stl))
        log.info("wrote STL:  %s", out_stl)


if __name__ == "__main__":
    app()
