#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "cadquery>=2.4",
#     "typer>=0.12",
#     "rich>=13",
# ]
# ///
"""Build mirrored screw-on tenting wedges from Ergogen DXF outlines.

The wedge reuses the case's mounting holes. It is modeled with a flat mating
surface, then rotated so its desk-facing surface is horizontal for printing.
The left half rises toward +X; the mirrored right half rises toward -X.

Examples:
  ./build_tenting_wedge.py build --dxf-dir ../output/outlines --angle 10 \
      --out-dir ../output/cases
  ./build_tenting_wedge.py inspect --dxf-dir ../output/outlines --angle 10
"""

from __future__ import annotations

import logging
import math
from pathlib import Path

import cadquery as cq
import typer
from cadquery import exporters, importers
from rich.logging import RichHandler

log = logging.getLogger("cq-tenting-wedge")
app = typer.Typer(add_completion=False, help=__doc__, no_args_is_help=True)


def _setup_logging(level: str) -> None:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(message)s",
        datefmt="[%H:%M:%S]",
        handlers=[
            RichHandler(
                rich_tracebacks=True,
                show_path=False,
                markup=False,
                keywords=[],
            )
        ],
    )
    logging.getLogger("ezdxf").setLevel(logging.WARNING)


def _closed_wires(dxf: Path) -> list[cq.Wire]:
    if not dxf.exists():
        raise FileNotFoundError(dxf)
    wires = importers.importDXF(str(dxf)).wires().vals()
    closed = [wire for wire in wires if isinstance(wire, cq.Wire) and wire.Closed()]
    if not closed:
        raise RuntimeError(f"no closed wires in {dxf}")
    return closed


def _wire_area(wire: cq.Wire) -> float:
    return cq.Face.makeFromWires(wire).Area()


def _outer_wire(dxf: Path) -> cq.Wire:
    return max(_closed_wires(dxf), key=_wire_area)


def _offset_wire(wire: cq.Wire, distance: float) -> cq.Wire:
    offset = cq.Workplane("XY").add(wire).toPending().offset2D(distance)
    wires = [item for item in offset.wires().vals() if isinstance(item, cq.Wire)]
    if not wires:
        raise RuntimeError(f"offset of {distance} mm removed the wedge interior")
    return max(wires, key=_wire_area)


def _wedge_envelope(
    wire: cq.Wire,
    min_height: float,
    angle: float,
) -> tuple[cq.Workplane, float]:
    """Return a solid whose top is Z=0 and bottom falls toward +X."""
    bounds = wire.BoundingBox()
    slope = math.tan(math.radians(angle))
    rise = bounds.xlen * slope
    max_height = min_height + rise
    margin = max(5.0, max_height)

    # Workplane("XZ") extrudes in -Y, so start beyond ymax and extrude far
    # enough to cover the complete outline.
    profile = (
        cq.Workplane("XZ")
        .moveTo(bounds.xmin - margin, 0)
        .lineTo(bounds.xmax + margin, 0)
        .lineTo(bounds.xmax + margin, -(max_height + margin * slope))
        .lineTo(bounds.xmin - margin, -(min_height - margin * slope))
        .close()
        .extrude(bounds.ylen + 2 * margin)
        .translate((0, bounds.ymax + margin, 0))
    )
    return profile, max_height


def _wire_prism(wire: cq.Wire, depth: float) -> cq.Workplane:
    face = cq.Face.makeFromWires(wire)
    return cq.Workplane("XY").add(face).extrude(-depth)


def _hole_centers(holes_dxf: Path) -> list[tuple[float, float]]:
    centers: list[tuple[float, float]] = []
    for wire in _closed_wires(holes_dxf):
        bounds = wire.BoundingBox()
        centers.append(
            (
                (bounds.xmin + bounds.xmax) / 2,
                (bounds.ymin + bounds.ymax) / 2,
            )
        )
    return centers


def _through_holes(holes_dxf: Path, max_height: float) -> cq.Workplane:
    solids: list[cq.Workplane] = []
    for wire in _closed_wires(holes_dxf):
        face = cq.Face.makeFromWires(wire)
        solids.append(
            cq.Workplane("XY", origin=(0, 0, 1)).add(face).extrude(-(max_height + 2))
        )
    result = solids[0]
    for solid in solids[1:]:
        result = result.union(solid)
    return result


def _rib_to_nearest_edge(
    x: float,
    y: float,
    outer: cq.Wire,
    outer_solid: cq.Workplane,
    width: float,
    boss_radius: float,
    max_height: float,
) -> cq.Workplane:
    """Connect a screw boss to the nearest perimeter with a printable web."""
    bounds = outer.BoundingBox()
    distances = {
        "left": x - bounds.xmin,
        "right": bounds.xmax - x,
        "bottom": y - bounds.ymin,
        "top": bounds.ymax - y,
    }
    edge = min(distances, key=lambda name: distances[name])

    if edge == "left":
        x0, x1 = bounds.xmin, x + boss_radius
        y0, y1 = y - width / 2, y + width / 2
    elif edge == "right":
        x0, x1 = x - boss_radius, bounds.xmax
        y0, y1 = y - width / 2, y + width / 2
    elif edge == "bottom":
        x0, x1 = x - width / 2, x + width / 2
        y0, y1 = bounds.ymin, y + boss_radius
    else:
        x0, x1 = x - width / 2, x + width / 2
        y0, y1 = y - boss_radius, bounds.ymax

    rib = (
        cq.Workplane("XY")
        .center((x0 + x1) / 2, (y0 + y1) / 2)
        .rect(x1 - x0, y1 - y0)
        .extrude(-(max_height + 1))
    )
    return rib.intersect(outer_solid)


def _build_wedge(
    outer_dxf: Path,
    holes_dxf: Path,
    angle: float,
    min_height: float,
    wall: float,
    boss_diameter: float,
    head_diameter: float,
    seat_thickness: float,
) -> cq.Workplane:
    if not 0 < angle < 30:
        raise ValueError("angle must be greater than 0 and less than 30 degrees")
    if min_height <= seat_thickness + 1:
        raise ValueError("min height must leave room below the screw seat")
    if wall <= 0 or boss_diameter <= head_diameter:
        raise ValueError(
            "wall must be positive and boss diameter must exceed head diameter"
        )

    outer = _outer_wire(outer_dxf)
    inner = _offset_wire(outer, -wall)
    envelope, max_height = _wedge_envelope(outer, min_height, angle)

    outer_solid = _wire_prism(outer, max_height + 1).intersect(envelope)
    inner_solid = _wire_prism(inner, max_height + 1).intersect(envelope)
    wedge = outer_solid.cut(inner_solid)

    # Keep the center open for support-free printing. Each boss gets a vertical
    # web to the nearest perimeter instead of a broad skin that would have to
    # bridge the full interior of the wedge.
    centers = _hole_centers(holes_dxf)
    for x, y in centers:
        boss = (
            cq.Workplane("XY")
            .center(x, y)
            .circle(boss_diameter / 2)
            .extrude(-(max_height + 1))
            .intersect(envelope)
        )
        rib = _rib_to_nearest_edge(
            x,
            y,
            outer,
            outer_solid,
            wall,
            boss_diameter / 2,
            max_height,
        )
        wedge = wedge.union(boss).union(rib)

    wedge = wedge.cut(_through_holes(holes_dxf, max_height))

    # Deep access counterbores leave the same material thickness under every
    # mounting point. This lets all four positions use one screw length even
    # though the wedge itself gets taller toward the inner edge.
    for x, y in centers:
        counterbore_top = -seat_thickness
        cutter_bottom = -(max_height + 2)
        counterbore = (
            cq.Workplane("XY", origin=(0, 0, cutter_bottom))
            .center(x, y)
            .circle(head_diameter / 2)
            .extrude(counterbore_top - cutter_bottom)
        )
        wedge = wedge.cut(counterbore)

    # Flatten the sloped underside onto Z=0 for printing. The mating surface
    # now rises toward +X by `angle`, which tents the left keyboard half.
    wedge = wedge.rotate((0, 0, 0), (0, 1, 0), -angle)
    zmin = wedge.val().BoundingBox().zmin
    return wedge.translate((0, 0, -zmin))


def _describe(
    outer_dxf: Path, angle: float, min_height: float
) -> tuple[float, float, float]:
    bounds = _outer_wire(outer_dxf).BoundingBox()
    rise = bounds.xlen * math.tan(math.radians(angle))
    return bounds.xlen, rise, min_height + rise


@app.command()
def build(
    dxf_dir: Path = typer.Option(
        ..., "--dxf-dir", help="Ergogen output/outlines directory."
    ),
    angle: float = typer.Option(10.0, "--angle", help="Tenting angle in degrees."),
    min_height: float = typer.Option(
        4.0, "--min-height", help="Low-edge wedge height in mm."
    ),
    wall: float = typer.Option(2.4, "--wall", help="Perimeter frame thickness in mm."),
    boss_diameter: float = typer.Option(
        8.0, "--boss-diameter", help="Mounting-hole boss diameter in mm."
    ),
    head_diameter: float = typer.Option(
        6.0, "--head-diameter", help="Screw-head counterbore diameter in mm."
    ),
    seat_thickness: float = typer.Option(
        2.0,
        "--seat-thickness",
        help="Material left between each screw-head seat and the case in mm.",
    ),
    out_dir: Path = typer.Option(
        ..., "--out-dir", help="Directory for left/right STEP and STL files."
    ),
    log_level: str = typer.Option("INFO", "--log-level", help="Python logging level."),
) -> None:
    """Generate printable left and mirrored-right screw-on wedges."""
    _setup_logging(log_level)
    outer_dxf = dxf_dir / "case_outer_ol.dxf"
    holes_dxf = dxf_dir / "holes_ol.dxf"

    try:
        left = _build_wedge(
            outer_dxf,
            holes_dxf,
            angle,
            min_height,
            wall,
            boss_diameter,
            head_diameter,
            seat_thickness,
        )
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        log.error("cannot build tenting wedge: %s", exc)
        raise typer.Exit(code=1) from exc

    right = left.val().mirror("YZ")
    out_dir.mkdir(parents=True, exist_ok=True)
    outputs = {
        "tenting_wedge_left.step": left,
        "tenting_wedge_left.stl": left,
        "tenting_wedge_right.step": right,
        "tenting_wedge_right.stl": right,
    }
    for name, shape in outputs.items():
        path = out_dir / name
        exporters.export(shape, str(path))
        log.info("wrote: %s", path)

    width, rise, max_height = _describe(outer_dxf, angle, min_height)
    log.info(
        "tenting summary: %.1f° across %.1f mm; rise %.1f mm; maximum height %.1f mm",
        angle,
        width,
        rise,
        max_height,
    )


@app.command()
def inspect(
    dxf_dir: Path = typer.Option(
        ..., "--dxf-dir", help="Ergogen output/outlines directory."
    ),
    angle: float = typer.Option(10.0, "--angle", help="Tenting angle in degrees."),
    min_height: float = typer.Option(
        4.0, "--min-height", help="Low-edge wedge height in mm."
    ),
    log_level: str = typer.Option("INFO", "--log-level", help="Python logging level."),
) -> None:
    """Report the wedge dimensions without writing files."""
    _setup_logging(log_level)
    try:
        width, rise, max_height = _describe(
            dxf_dir / "case_outer_ol.dxf", angle, min_height
        )
        holes = _hole_centers(dxf_dir / "holes_ol.dxf")
    except (FileNotFoundError, RuntimeError) as exc:
        log.error("cannot inspect tenting wedge: %s", exc)
        raise typer.Exit(code=1) from exc

    log.info("case width: %.1f mm", width)
    log.info("tenting angle: %.1f°", angle)
    log.info("inner-edge rise: %.1f mm", rise)
    log.info("wedge height: %.1f–%.1f mm", min_height, max_height)
    log.info("mounting holes: %d", len(holes))


if __name__ == "__main__":
    app()
