#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11,<3.13"
# dependencies = [
#     "cadquery>=2.4",
#     "typer>=0.12",
#     "rich>=13",
# ]
# ///
"""Build a face-to-face transport separator from the keyboard perimeter.

The separator follows the case wall outline and overlaps the PCB edge slightly,
so each keyboard half bears on an end of the ring instead of on its keycaps.
The default 18 mm height clears two 8.05 mm Choc assembly envelopes by 1.9 mm.

Example:
  ./build_transport_wall.py --wall-ring-dxf output/outlines/wall_ring_ol.dxf \
      --height 18 --pcb-overlap 0.8 \
      --out-step output/cases/transport_separator_wall.step \
      --out-stl output/cases/transport_separator_wall.stl
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Annotated

import cadquery as cq
import typer
from cadquery import exporters, importers
from rich.logging import RichHandler

log = logging.getLogger("cq-transport-wall")
app = typer.Typer(add_completion=False, help=__doc__, no_args_is_help=True)


def _setup_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(message)s",
        datefmt="[%H:%M:%S]",
        handlers=[
            RichHandler(
                rich_tracebacks=True, show_path=False, markup=False, keywords=[]
            )
        ],
    )


def _closed_wires(dxf: Path) -> list[cq.Wire]:
    wires = [
        wire
        for wire in importers.importDXF(str(dxf)).wires().vals()
        if isinstance(wire, cq.Wire) and wire.Closed()
    ]
    if len(wires) != 2:
        raise ValueError(f"expected outer and PCB wires in {dxf}, found {len(wires)}")
    return sorted(
        wires, key=lambda wire: cq.Face.makeFromWires(wire).Area(), reverse=True
    )


def build_separator(
    wall_ring_dxf: Path, height: float, pcb_overlap: float
) -> cq.Workplane:
    """Extrude the perimeter ring, extending it inward over the PCB edge."""
    if height <= 0:
        raise ValueError("height must be positive")
    if pcb_overlap < 0:
        raise ValueError("pcb overlap cannot be negative")

    outer_wire, pcb_wire = _closed_wires(wall_ring_dxf)
    inner_wires = pcb_wire.offset2D(-pcb_overlap) if pcb_overlap else [pcb_wire]
    if len(inner_wires) != 1:
        raise ValueError(
            f"PCB inset produced {len(inner_wires)} wires; expected one continuous perimeter"
        )

    face = cq.Face.makeFromWires(outer_wire, [inner_wires[0]])
    return cq.Workplane("XY").add(face).extrude(height)


@app.command()
def main(
    wall_ring_dxf: Annotated[
        Path, typer.Option("--wall-ring-dxf", help="Ergogen wall_ring_ol.dxf path.")
    ],
    out_step: Annotated[Path, typer.Option("--out-step", help="Output STEP path.")],
    height: Annotated[
        float,
        typer.Option(
            "--height",
            min=1.2,
            help="PCB-to-PCB separation in mm; 18 mm clears two Choc assemblies.",
        ),
    ] = 18.0,
    pcb_overlap: Annotated[
        float,
        typer.Option(
            "--pcb-overlap",
            min=0.0,
            help="Inward overlap onto the PCB perimeter in mm.",
        ),
    ] = 0.8,
    out_stl: Annotated[
        Path | None, typer.Option("--out-stl", help="Optional STL path.")
    ] = None,
    log_level: Annotated[
        str, typer.Option("--log-level", help="Python logging level.")
    ] = "INFO",
) -> None:
    _setup_logging(log_level)
    separator = build_separator(wall_ring_dxf, height, pcb_overlap)
    bounds = separator.val().BoundingBox()

    out_step.parent.mkdir(parents=True, exist_ok=True)
    exporters.export(separator, str(out_step))
    log.info("wrote STEP: %s", out_step)

    if out_stl:
        out_stl.parent.mkdir(parents=True, exist_ok=True)
        exporters.export(separator, str(out_stl), tolerance=0.01, angularTolerance=0.1)
        log.info("wrote STL:  %s", out_stl)

    log.info(
        "dimensions: %.1f x %.1f x %.1f mm; volume: %.0f mm³",
        bounds.xlen,
        bounds.ylen,
        bounds.zlen,
        separator.val().Volume(),
    )


if __name__ == "__main__":
    app()
