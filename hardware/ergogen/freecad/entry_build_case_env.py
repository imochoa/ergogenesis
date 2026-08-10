# FreeCAD entrypoint: build case using environment variables
# Env vars:
#   DXF_DIR, BOTTOM_TH, STANDOFF_H, WALL_H, OUT_STEP, OUT_STL, LINEAR_DEFL (opt)

import os
import sys

import FreeCAD as App  # noqa: F401

# Ensure neighbor modules are importable
sys.path.insert(0, os.path.dirname(__file__))

from build_case import (
    extrude_union,
    extrude_union_optional,
    export_step_and_stl,
)


def main():
    dxf_dir = os.environ.get("DXF_DIR")
    bottom_th = float(os.environ.get("BOTTOM_TH", "0"))
    standoff_h = float(os.environ.get("STANDOFF_H", "0"))
    wall_h = float(os.environ.get("WALL_H", "0"))
    out_step = os.environ.get("OUT_STEP")
    out_stl = os.environ.get("OUT_STL")
    lin_defl = float(os.environ.get("LINEAR_DEFL", "0.05"))

    if not dxf_dir or not out_step:
        sys.stderr.write("DXF_DIR and OUT_STEP env vars are required.\n")
        raise SystemExit(2)

    from pathlib import Path

    dxf_dir = Path(dxf_dir)
    case_base_dxf = dxf_dir / "case_base_ol.dxf"
    wall_ring_dxf = dxf_dir / "wall_ring_ol.dxf"
    standoff_dxf = dxf_dir / "standoff_ol.dxf"
    holes_dxf = dxf_dir / "holes_ol.dxf"
    switch_cut_dxf = dxf_dir / "switch_wall_cutout_ol.dxf"
    usb_cut_dxf = dxf_dir / "usb_wall_cutout_ol.dxf"

    full_h = bottom_th + standoff_h + wall_h

    base = extrude_union(str(case_base_dxf), bottom_th)
    walls = extrude_union(str(wall_ring_dxf), full_h)
    standoffs = extrude_union(str(standoff_dxf), bottom_th + standoff_h)

    case = base.fuse(walls)
    case = case.fuse(standoffs)

    holes = extrude_union(str(holes_dxf), full_h)
    case = case.cut(holes)

    sw_cut = extrude_union_optional(str(switch_cut_dxf), full_h)
    if sw_cut:
        case = case.cut(sw_cut)
    usb_cut = extrude_union_optional(str(usb_cut_dxf), full_h)
    if usb_cut:
        case = case.cut(usb_cut)

    try:
        case = case.removeSplitter()
    except Exception:
        pass

    export_step_and_stl(case, out_step, out_stl, lin_defl)


if __name__ == "__main__":
    main()
