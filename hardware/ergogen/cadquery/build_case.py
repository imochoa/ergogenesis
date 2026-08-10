#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "cadquery>=2.4",
#     "typer>=0.12",
#     "rich>=13",
# ]
# ///
"""Build full case (base + walls + standoffs - holes - cutouts) from DXFs using CadQuery.

Examples:
  ./build_case.py run --dxf-dir output/outlines --bottom-th 2.0 --standoff-h 2.0 --wall-h 5.0 \
      --out-step output/cases/case_cq.step --out-stl output/cases/case_cq.stl
"""

from __future__ import annotations

import logging
from pathlib import Path

import cadquery as cq
from cadquery import exporters, importers
import typer
from rich.logging import RichHandler

log = logging.getLogger("cq-case")
app = typer.Typer(add_completion=False, help=__doc__, no_args_is_help=True)


def _setup_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(message)s",
        datefmt="[%H:%M:%S]",
        handlers=[RichHandler(rich_tracebacks=True, show_path=False, markup=False, keywords=[])],
    )


def _load_wires(dxf: Path) -> list[cq.Wire]:
    wp = importers.importDXF(str(dxf))
    wires_wp = wp.wires()
    return [w for w in wires_wp.vals() if isinstance(w, cq.Wire) and w.Closed()]


def _extrude_union(dxf: Path, height: float) -> cq.Workplane:
    wires = _load_wires(dxf)
    if not wires:
        raise RuntimeError(f"no closed wires in {dxf}")
    solids: list[cq.Workplane] = []
    for w in wires:
        try:
            f = cq.Face.makeFromWires(w)
            solids.append(cq.Workplane("XY").add(f).extrude(height))
        except Exception:
            pass
    if not solids:
        raise RuntimeError(f"no solids extruded from {dxf}")
    result = solids[0]
    for s in solids[1:]:
        result = result.union(s)
    return result


def _solid_with_holes(dxf: Path, height: float) -> cq.Workplane:
    """Extrude a single region with holes: largest wire as outer, rest as holes."""
    wires = _load_wires(dxf)
    if not wires:
        raise RuntimeError(f"no wires in {dxf}")
    # sort by area descending on their face proxies
    faces = []
    for w in wires:
        try:
            f = cq.Face.makeFromWires(w)
            faces.append((f.Area(), w))  # type: ignore[attr-defined]
        except Exception:
            pass
    if not faces:
        raise RuntimeError(f"no faces from wires in {dxf}")
    faces.sort(key=lambda t: t[0], reverse=True)
    outer_wire = faces[0][1]
    hole_wires = [w for _, w in faces[1:]]
    face = cq.Face.makeFromWires(outer_wire, hole_wires)
    return cq.Workplane("XY").add(face).extrude(height)


def _extrude_optional(dxf: Path, height: float) -> cq.Workplane | None:
    if not dxf.exists():
        log.info("(optional) missing: %s", dxf)
        return None
    return _extrude_union(dxf, height)


@app.command()
def run(
    dxf_dir: Path = typer.Option(..., "--dxf-dir", help="Directory with DXFs (ergogen/output/outlines)"),
    bottom_th: float = typer.Option(..., "--bottom-th", help="Base plate thickness (mm)"),
    standoff_h: float = typer.Option(..., "--standoff-h", help="Standoff height (mm)"),
    wall_h: float = typer.Option(..., "--wall-h", help="Wall height above standoffs (mm)"),
    out_step: Path = typer.Option(..., "--out-step", help="Output STEP path"),
    out_stl: Path = typer.Option(None, "--out-stl", help="Optional STL path"),
    log_level: str = typer.Option("INFO", "--log-level", help="Python logging level"),
):
    _setup_logging(log_level)
    case_base_dxf = dxf_dir / "case_base_ol.dxf"
    wall_ring_dxf = dxf_dir / "wall_ring_ol.dxf"
    standoff_dxf = dxf_dir / "standoff_ol.dxf"
    holes_dxf = dxf_dir / "holes_ol.dxf"
    switch_cut_dxf = dxf_dir / "switch_wall_cutout_ol.dxf"
    usb_cut_dxf = dxf_dir / "usb_wall_cutout_ol.dxf"

    full_h = bottom_th + standoff_h + wall_h

    base = _solid_with_holes(case_base_dxf, bottom_th)
    walls = _solid_with_holes(wall_ring_dxf, full_h)
    standoffs = _extrude_union(standoff_dxf, bottom_th + standoff_h)

    case = base.union(walls).union(standoffs)

    holes = _extrude_union(holes_dxf, full_h)
    case = case.cut(holes)

    sw = _extrude_optional(switch_cut_dxf, full_h)
    if sw:
        case = case.cut(sw)
    usb = _extrude_optional(usb_cut_dxf, full_h)
    if usb:
        case = case.cut(usb)

    out_step.parent.mkdir(parents=True, exist_ok=True)
    exporters.export(case, str(out_step))
    log.info("wrote STEP: %s", out_step)
    if out_stl:
        exporters.export(case, str(out_stl))
        log.info("wrote STL:  %s", out_stl)


if __name__ == "__main__":
    app()
