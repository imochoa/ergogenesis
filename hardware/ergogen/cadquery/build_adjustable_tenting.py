#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "cadquery>=2.4",
#     "typer>=0.12",
#     "rich>=13",
# ]
# ///
"""Build an adjustable, card-braced tenting case for both keyboard halves.

Shallow indexed grooves are cut directly into the case underside. The case's
existing outer wall seats against a sloped edge guide on the floor plate and
acts as the pivot, so no separate mounting plate or protruding hinge is needed.
One tapered support card is reused for every configured angle.

Examples:
  ./build_adjustable_tenting.py build --config ../config.yaml \
      --dxf-dir ../output/outlines --out-dir ../output/cases
  ./build_adjustable_tenting.py inspect --config ../config.yaml \
      --dxf-dir ../output/outlines
"""

from __future__ import annotations

import logging
import math
import re
from dataclasses import dataclass
from pathlib import Path

import cadquery as cq
import typer
from build_case import _extrude_optional, _extrude_union, _solid_with_holes
from cadquery import exporters, importers
from rich.logging import RichHandler

log = logging.getLogger("cq-adjustable-tenting")
app = typer.Typer(add_completion=False, help=__doc__, no_args_is_help=True)


@dataclass(frozen=True)
class Settings:
    bottom_thickness: float
    standoff_height: float
    wall_height: float
    floor_thickness: float
    floor_margin: float
    case_corner_radius: float
    floor_corner_radius: float
    edge_guide_height: float
    edge_clearance: float
    edge_wall_thickness: float
    edge_return_depth: float
    card_length: float
    card_width: float
    card_y_shift: float
    card_thickness: float
    card_tip_thickness: float
    card_taper_length: float
    card_tab_length: float
    groove_width: float
    groove_depth: float
    slot_clearance: float
    angle_min: int
    angle_max: int
    angle_step: int


@dataclass(frozen=True)
class SlotPair:
    angle: int
    case_distance: float
    floor_distance: float
    card_angle: float


UNIT_KEYS = {
    "bottom_plate_thickness": "bottom_thickness",
    "standoff_height": "standoff_height",
    "wall_height": "wall_height",
    "tenting_floor_thickness": "floor_thickness",
    "tenting_floor_margin": "floor_margin",
    "tenting_case_corner_radius": "case_corner_radius",
    "tenting_floor_corner_radius": "floor_corner_radius",
    "tenting_edge_guide_height": "edge_guide_height",
    "tenting_edge_clearance": "edge_clearance",
    "tenting_edge_wall_thickness": "edge_wall_thickness",
    "tenting_edge_return_depth": "edge_return_depth",
    "tenting_card_length": "card_length",
    "tenting_card_width": "card_width",
    "tenting_card_y_shift": "card_y_shift",
    "tenting_card_thickness": "card_thickness",
    "tenting_card_tip_thickness": "card_tip_thickness",
    "tenting_card_taper_length": "card_taper_length",
    "tenting_card_tab_length": "card_tab_length",
    "tenting_groove_width": "groove_width",
    "tenting_groove_depth": "groove_depth",
    "tenting_slot_clearance": "slot_clearance",
    "tenting_angle_min": "angle_min",
    "tenting_angle_max": "angle_max",
    "tenting_angle_step": "angle_step",
}


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


def _settings(config: Path) -> Settings:
    text = config.read_text()
    values: dict[str, float] = {}
    for unit, field in UNIT_KEYS.items():
        match = re.search(
            rf"^\s*{re.escape(unit)}:\s*([0-9.]+)\s*(?:#.*)?$",
            text,
            re.MULTILINE,
        )
        if not match:
            raise ValueError(f"missing numeric unit {unit} in {config}")
        values[field] = float(match.group(1))

    for field in ("angle_min", "angle_max", "angle_step"):
        values[field] = int(values[field])
    return Settings(**values)  # type: ignore[arg-type]


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
    # Intersection joins remain valid around this concave outline. Acute
    # exterior miters are rounded explicitly after clipping their excess.
    offset = (
        cq.Workplane("XY").add(wire).toPending().offset2D(distance, kind="intersection")
    )
    wires = [item for item in offset.wires().vals() if isinstance(item, cq.Wire)]
    if not wires:
        raise RuntimeError(f"offset of {distance} mm removed the floor outline")
    return max(wires, key=_wire_area)


def _line_intersection(
    a: cq.Vector,
    b: cq.Vector,
    c: cq.Vector,
    d: cq.Vector,
) -> cq.Vector:
    denominator = (a.x - b.x) * (c.y - d.y) - (a.y - b.y) * (c.x - d.x)
    if abs(denominator) < 1e-9:
        raise RuntimeError("cannot reconstruct parallel corner edges")
    ab_cross = a.x * b.y - a.y * b.x
    cd_cross = c.x * d.y - c.y * d.x
    return cq.Vector(
        (ab_cross * (c.x - d.x) - (a.x - b.x) * cd_cross) / denominator,
        (ab_cross * (c.y - d.y) - (a.y - b.y) * cd_cross) / denominator,
        0,
    )


def _refillet_lowest_corner(wire: cq.Wire, radius: float) -> cq.Wire:
    """Replace the undersized lowest outside arc with one continuous fillet."""
    edges = wire.Edges()
    arc_index = min(
        (index for index, edge in enumerate(edges) if edge.geomType() == "CIRCLE"),
        key=lambda index: edges[index].BoundingBox().ymin,
    )
    previous = edges[arc_index - 1]
    arc = edges[arc_index]
    following = edges[arc_index + 1]
    if previous.geomType() != "LINE" or following.geomType() != "LINE":
        raise RuntimeError("lowest case corner is not bounded by straight edges")

    def shared_vertex(first: cq.Edge, second: cq.Edge) -> tuple[cq.Vertex, cq.Vertex]:
        return min(
            ((left, right) for left in first.Vertices() for right in second.Vertices()),
            key=lambda pair: pair[0].distance(pair[1]),
        )

    previous_end, _ = shared_vertex(previous, arc)
    _, following_start = shared_vertex(arc, following)
    previous_start = next(
        vertex for vertex in previous.Vertices() if vertex.distance(previous_end) > 1e-6
    )
    following_end = next(
        vertex
        for vertex in following.Vertices()
        if vertex.distance(following_start) > 1e-6
    )
    corner = _line_intersection(
        previous_start.Center(),
        previous_end.Center(),
        following_start.Center(),
        following_end.Center(),
    )

    rebuilt_edges: list[cq.Edge] = []
    for index, edge in enumerate(edges):
        if index == arc_index - 1:
            rebuilt_edges.append(cq.Edge.makeLine(previous_start.Center(), corner))
        elif index == arc_index:
            continue
        elif index == arc_index + 1:
            rebuilt_edges.append(cq.Edge.makeLine(corner, following_end.Center()))
        else:
            rebuilt_edges.append(edge)
    rebuilt = cq.Wire.assembleEdges(rebuilt_edges)
    corner_vertex = min(
        rebuilt.Vertices(),
        key=lambda vertex: vertex.Center().sub(corner).Length,
    )
    rounded = rebuilt.fillet2D(radius, [corner_vertex])
    if not cq.Face.makeFromWires(rounded).isValid():
        raise RuntimeError("rounded case corner produced an invalid outline")
    return rounded


def _fillet_min_x_vertical_edges(
    solid: cq.Workplane,
    radius: float,
) -> cq.Workplane:
    """Round transitions at the clipped outer pivot edge."""
    x_min = solid.val().BoundingBox().xmin
    edges = [
        edge
        for edge in solid.edges().vals()
        if edge.geomType() == "LINE"
        and edge.BoundingBox().zlen > 0.1
        and abs(edge.BoundingBox().xmin - x_min) < 1e-5
    ]
    if not edges:
        raise RuntimeError("could not find pivot-edge corners to round")
    return solid.newObject(edges).fillet(radius)


def _wire_prism(wire: cq.Wire, height: float) -> cq.Workplane:
    return cq.Workplane("XY").add(cq.Face.makeFromWires(wire)).extrude(height)


def _angles(settings: Settings) -> list[int]:
    if settings.angle_step <= 0 or settings.angle_min <= 0:
        raise ValueError("tenting angles and step must be positive")
    if settings.angle_max < settings.angle_min:
        raise ValueError("maximum tenting angle must not be below the minimum")
    return list(range(settings.angle_min, settings.angle_max + 1, settings.angle_step))


def _slot_pairs(settings: Settings) -> list[SlotPair]:
    pairs: list[SlotPair] = []
    for angle in _angles(settings):
        radians = math.radians(angle)
        # Keep the same short card vertical at every angle. The case groove is
        # placed H/sin(angle) from the pivot and the floor groove directly
        # below it at H/tan(angle), where H is the card's contact length.
        case_distance = settings.card_length / math.sin(radians)
        floor_distance = settings.card_length / math.tan(radians)
        pairs.append(SlotPair(angle, case_distance, floor_distance, 90.0))
    return pairs


def _groove_cutter(
    x: float,
    y: float,
    z: float,
    width: float,
    length: float,
    depth: float,
) -> cq.Workplane:
    return (
        cq.Workplane("XY", origin=(0, 0, z))
        .center(x, y)
        .rect(width, length)
        .extrude(depth)
    )


def _index_markers(
    x: float,
    y: float,
    z: float,
    depth: float,
    count: int,
) -> cq.Workplane:
    """Return one-to-five shallow dots identifying a matching groove pair."""
    spacing = 1.5
    cutters: list[cq.Workplane] = []
    for index in range(count):
        dot_y = y + (index - (count - 1) / 2) * spacing
        cutters.append(
            cq.Workplane("XY", origin=(0, 0, z))
            .center(x, dot_y)
            .circle(0.45)
            .extrude(depth)
        )
    result = cutters[0]
    for cutter in cutters[1:]:
        result = result.union(cutter)
    return result


def _base_case(
    dxf_dir: Path,
    settings: Settings,
    case_inner: cq.Wire,
    case_outer: cq.Wire,
) -> cq.Workplane:
    full_height = (
        settings.bottom_thickness + settings.standoff_height + settings.wall_height
    )
    base = _solid_with_holes(dxf_dir / "case_base_ol.dxf", settings.bottom_thickness)
    wall_face = cq.Face.makeFromWires(case_outer, [case_inner])
    walls = cq.Workplane("XY").add(wall_face).extrude(full_height)
    standoffs = _extrude_union(
        dxf_dir / "standoff_ol.dxf",
        settings.bottom_thickness + settings.standoff_height,
    )
    case = base.union(walls).union(standoffs)
    case = case.cut(_extrude_union(dxf_dir / "holes_ol.dxf", full_height))

    for name in ("switch_wall_cutout_ol.dxf", "usb_wall_cutout_ol.dxf"):
        cutter = _extrude_optional(dxf_dir / name, full_height)
        if cutter:
            case = case.cut(cutter)
    return case


def _case_with_grooves(
    dxf_dir: Path,
    settings: Settings,
    pairs: list[SlotPair],
    pivot_x: float,
    brace_y: float,
    case_inner: cq.Wire,
    case_outer: cq.Wire,
) -> cq.Workplane:
    case = _base_case(dxf_dir, settings, case_inner, case_outer)
    groove_length = settings.card_width + 2 * settings.slot_clearance
    marker_y = brace_y + settings.card_width / 2 + 4.5
    for index, pair in enumerate(pairs, start=1):
        groove_x = pivot_x + pair.case_distance
        case = case.cut(
            _groove_cutter(
                groove_x,
                brace_y,
                -0.05,
                settings.groove_width,
                groove_length,
                settings.groove_depth + 0.05,
            )
        ).cut(_index_markers(groove_x, marker_y, -0.05, 0.4, index))
    return case


def _edge_guide(
    case_outer: cq.Wire,
    settings: Settings,
    pivot_x: float,
) -> cq.Workplane:
    """Build a raised U-shaped guide following the actual case contour."""
    dynamic_clearance = settings.edge_clearance + settings.edge_guide_height * math.tan(
        math.radians(settings.angle_max)
    )
    inner = _offset_wire(case_outer, dynamic_clearance)
    outer = _offset_wire(inner, settings.edge_wall_thickness)
    guide_face = cq.Face.makeFromWires(outer, [inner])
    guide = (
        cq.Workplane("XY")
        .add(guide_face)
        .extrude(settings.edge_guide_height)
        .translate((0, 0, settings.floor_thickness))
    )

    # Clip the acute offset miter at its intended distance, then round both
    # transitions into the contour-following returns.
    bounds = outer.BoundingBox()
    x_min = pivot_x - dynamic_clearance - settings.edge_wall_thickness
    x_max = pivot_x + settings.edge_return_depth
    clip = cq.Workplane(
        "XY",
        origin=(
            (x_min + x_max) / 2,
            (bounds.ymin + bounds.ymax) / 2,
            settings.floor_thickness,
        ),
    ).box(
        x_max - x_min,
        bounds.ylen + 2,
        settings.edge_guide_height + 0.1,
        centered=(True, True, False),
    )
    clipped = guide.intersect(clip)
    continuous_wall = max(clipped.solids().vals(), key=lambda solid: solid.Volume())
    return _fillet_min_x_vertical_edges(
        cq.Workplane("XY").newObject([continuous_wall]),
        min(settings.floor_corner_radius, settings.edge_wall_thickness / 2),
    )


def _floor_plate(
    case_outer: cq.Wire,
    floor_outer: cq.Wire,
    settings: Settings,
    pairs: list[SlotPair],
    pivot_x: float,
    brace_y: float,
) -> cq.Workplane:
    floor = _wire_prism(floor_outer, settings.floor_thickness)

    # Clip only the acute offset's miter spike, then fillet the two resulting
    # vertical corners so the outside floor contour remains continuously round.
    bounds = floor.val().BoundingBox()
    floor_x_min = pivot_x - settings.floor_margin
    floor_clip = cq.Workplane(
        "XY",
        origin=(
            (floor_x_min + bounds.xmax + 1) / 2,
            (bounds.ymin + bounds.ymax) / 2,
            0,
        ),
    ).box(
        bounds.xmax + 1 - floor_x_min,
        bounds.ylen + 2,
        settings.floor_thickness + 0.1,
        centered=(True, True, False),
    )
    floor = _fillet_min_x_vertical_edges(
        floor.intersect(floor_clip),
        settings.floor_corner_radius,
    )

    groove_length = settings.card_width + 2 * settings.slot_clearance
    groove_z = settings.floor_thickness - settings.groove_depth
    marker_y = brace_y + settings.card_width / 2 + 4.5
    for index, pair in enumerate(pairs, start=1):
        groove_x = pivot_x + pair.floor_distance
        floor = floor.cut(
            _groove_cutter(
                groove_x,
                brace_y,
                groove_z,
                settings.groove_width,
                groove_length,
                settings.groove_depth + 0.05,
            )
        ).cut(
            _index_markers(
                groove_x,
                marker_y,
                settings.floor_thickness - 0.4,
                0.45,
                index,
            )
        )
    return floor.union(_edge_guide(case_outer, settings, pivot_x))


def _support_card(settings: Settings) -> cq.Workplane:
    half = settings.card_thickness / 2
    tip = settings.card_tip_thickness
    taper = settings.card_taper_length
    tab = settings.card_tab_length
    length = settings.card_length
    if taper * 2 >= length:
        raise ValueError("card taper lengths consume the complete card")
    if tab <= 0 or tip <= 0 or tip >= settings.groove_width:
        raise ValueError("card tabs must be positive and narrower than their grooves")
    tip_half = tip / 2
    return (
        cq.Workplane("XZ")
        # Symmetric tapered tabs locate the short vertical card in matching
        # case and floor grooves without introducing a horizontal thrust load.
        .moveTo(-tip_half, -tab)
        .lineTo(tip_half, -tab)
        .lineTo(tip_half, 0)
        .lineTo(half, taper)
        .lineTo(half, length - taper)
        .lineTo(tip_half, length)
        .lineTo(tip_half, length + tab)
        .lineTo(-tip_half, length + tab)
        .lineTo(-tip_half, length)
        .lineTo(-half, length - taper)
        .lineTo(-half, taper)
        .lineTo(-tip_half, 0)
        .close()
        .extrude(settings.card_width)
        .translate((0, settings.card_width / 2, 0))
    )


def _printable_card(card: cq.Workplane) -> cq.Workplane:
    printable = card.rotate((0, 0, 0), (0, 1, 0), 90)
    bounds = printable.val().BoundingBox()
    return printable.translate((0, 0, -bounds.zmin))


def _case_at_angle(
    case: cq.Workplane,
    pivot_x: float,
    floor_z: float,
    angle: float,
) -> cq.Workplane:
    return case.rotate((pivot_x, 0, 0), (pivot_x, 1, 0), -angle).translate(
        (0, 0, floor_z)
    )


def _card_at_pair(
    card: cq.Workplane,
    pair: SlotPair,
    pivot_x: float,
    brace_y: float,
    floor_z: float,
) -> cq.Workplane:
    rotation = 90 - pair.card_angle
    return card.rotate((0, 0, 0), (0, 1, 0), rotation).translate(
        (pivot_x + pair.floor_distance, brace_y, floor_z)
    )


def _validate_geometry(
    case: cq.Workplane,
    floor: cq.Workplane,
    card: cq.Workplane,
    pairs: list[SlotPair],
    settings: Settings,
    pivot_x: float,
    brace_y: float,
) -> None:
    for name, part in (("case", case), ("floor", floor), ("card", card)):
        if not part.val().isValid() or part.solids().size() != 1:
            raise RuntimeError(f"{name} is not one valid solid")

    floor_z = settings.floor_thickness
    angles: list[tuple[int, cq.Workplane | None]] = [(0, None)]
    angles.extend(
        (
            pair.angle,
            _card_at_pair(card, pair, pivot_x, brace_y, floor_z),
        )
        for pair in pairs
    )
    for angle, positioned_card in angles:
        positioned_case = _case_at_angle(case, pivot_x, floor_z, angle)
        if floor.val().intersect(positioned_case.val()).Volume() > 1e-4:
            raise RuntimeError(f"floor and case collide at {angle}°")
        if positioned_card is None:
            continue
        if floor.val().intersect(positioned_card.val()).Volume() > 1e-4:
            raise RuntimeError(f"floor and support card collide at {angle}°")
        if positioned_case.val().intersect(positioned_card.val()).Volume() > 1e-4:
            raise RuntimeError(f"case and support card collide at {angle}°")


def _mirror(shape: cq.Workplane | cq.Shape) -> cq.Shape:
    item = shape.val() if isinstance(shape, cq.Workplane) else shape
    return item.mirror("YZ")


def _export(shape: cq.Workplane | cq.Shape, path: Path) -> None:
    if path.suffix.lower() == ".stl":
        exporters.export(shape, str(path), tolerance=0.01, angularTolerance=0.1)
    else:
        exporters.export(shape, str(path))
    log.info("wrote: %s", path)


def _build_geometry(
    dxf_dir: Path,
    settings: Settings,
) -> tuple[
    cq.Workplane,
    cq.Workplane,
    cq.Workplane,
    list[SlotPair],
    float,
    float,
]:
    case_inner = _outer_wire(dxf_dir / "case_base_ol.dxf")
    outer = _refillet_lowest_corner(
        _outer_wire(dxf_dir / "case_outer_ol.dxf"),
        settings.case_corner_radius,
    )
    floor_outer = _offset_wire(outer, settings.floor_margin)
    bounds = outer.BoundingBox()
    pivot_x = bounds.xmin
    brace_y = (bounds.ymin + bounds.ymax) / 2 + settings.card_y_shift
    pairs = _slot_pairs(settings)

    if pivot_x + max(pair.case_distance for pair in pairs) >= bounds.xmax:
        raise ValueError("case grooves extend beyond the case outline")

    case = _case_with_grooves(
        dxf_dir,
        settings,
        pairs,
        pivot_x,
        brace_y,
        case_inner,
        outer,
    )
    floor = _floor_plate(
        outer,
        floor_outer,
        settings,
        pairs,
        pivot_x,
        brace_y,
    )
    card = _support_card(settings)
    _validate_geometry(case, floor, card, pairs, settings, pivot_x, brace_y)
    return case, floor, card, pairs, pivot_x, brace_y


@app.command()
def build(
    config: Path = typer.Option(..., "--config", help="Ergogen config.yaml path."),
    dxf_dir: Path = typer.Option(
        ..., "--dxf-dir", help="Ergogen output/outlines directory."
    ),
    out_dir: Path = typer.Option(
        ..., "--out-dir", help="Directory for STEP and STL outputs."
    ),
    log_level: str = typer.Option("INFO", "--log-level", help="Python logging level."),
) -> None:
    """Generate printable parts and angle-specific assembly previews."""
    _setup_logging(log_level)
    try:
        settings = _settings(config)
        case, floor, card, pairs, pivot_x, brace_y = _build_geometry(dxf_dir, settings)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        log.error("cannot build adjustable tenting kit: %s", exc)
        raise typer.Exit(code=1) from exc

    out_dir.mkdir(parents=True, exist_ok=True)
    printable_card = _printable_card(card)
    parts: dict[str, cq.Workplane | cq.Shape] = {
        "adjustable_tenting_case_left": case,
        "adjustable_tenting_case_right": _mirror(case),
        "adjustable_tenting_floor_left": floor,
        "adjustable_tenting_floor_right": _mirror(floor),
        "adjustable_tenting_card": printable_card,
    }
    for name, shape in parts.items():
        _export(shape, out_dir / f"{name}.step")
        _export(shape, out_dir / f"{name}.stl")

    floor_z = settings.floor_thickness
    folded = cq.Compound.makeCompound(
        [floor.val(), _case_at_angle(case, pivot_x, floor_z, 0).val()]
    )
    _export(folded, out_dir / "adjustable_tenting_00deg_left.step")
    _export(folded.mirror("YZ"), out_dir / "adjustable_tenting_00deg_right.step")

    for pair in pairs:
        positioned_case = _case_at_angle(case, pivot_x, floor_z, pair.angle)
        positioned_card = _card_at_pair(
            card,
            pair,
            pivot_x,
            brace_y,
            floor_z,
        )
        left = cq.Compound.makeCompound(
            [floor.val(), positioned_case.val(), positioned_card.val()]
        )
        right = left.mirror("YZ")
        stem = f"adjustable_tenting_{pair.angle:02d}deg"
        _export(left, out_dir / f"{stem}_left.step")
        _export(right, out_dir / f"{stem}_right.step")

    log.info(
        "built %d angle positions (%d°–%d°) with one %.1f mm support card",
        len(pairs),
        pairs[0].angle,
        pairs[-1].angle,
        settings.card_length,
    )


@app.command()
def inspect(
    config: Path = typer.Option(..., "--config", help="Ergogen config.yaml path."),
    dxf_dir: Path = typer.Option(
        ..., "--dxf-dir", help="Ergogen output/outlines directory."
    ),
    log_level: str = typer.Option("INFO", "--log-level", help="Python logging level."),
) -> None:
    """Report computed slot pairs and validate all configured positions."""
    _setup_logging(log_level)
    try:
        settings = _settings(config)
        _, _, _, pairs, _, _ = _build_geometry(dxf_dir, settings)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        log.error("cannot inspect adjustable tenting kit: %s", exc)
        raise typer.Exit(code=1) from exc

    log.info("angle | case groove | floor groove | card angle")
    for pair in pairs:
        log.info(
            "%5d° | %11.2f | %12.2f | %9.2f°",
            pair.angle,
            pair.case_distance,
            pair.floor_distance,
            pair.card_angle,
        )


if __name__ == "__main__":
    app()
