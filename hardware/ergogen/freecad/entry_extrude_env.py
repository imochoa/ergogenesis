# FreeCAD entrypoint: extrude from DXF using environment variables
# Expected env vars:
#   DXF_PATH, HEIGHT_MM, OUT_STEP, OUT_STL, LINEAR_DEFL (optional)

import os
import sys

import FreeCAD as App  # noqa: F401

# Ensure we can import neighbor modules when invoked by FreeCAD
sys.path.insert(0, os.path.dirname(__file__))

from extrude_dxf import (
    build_solid_from_wires,
    export_step_and_stl,
    load_wires_from_dxf,
)


def main():
    try:
        dxf = os.environ.get("DXF_PATH")
        height = float(os.environ.get("HEIGHT_MM", "0"))
        out_step = os.environ.get("OUT_STEP")
        out_stl = os.environ.get("OUT_STL")
        lin_defl = float(os.environ.get("LINEAR_DEFL", "0.05"))
        if not dxf or not out_step:
            sys.stderr.write("DXF_PATH and OUT_STEP env vars are required.\n")
            raise SystemExit(2)
        print(f"DXF_PATH={dxf}")
        print(f"HEIGHT_MM={height}")
        print(f"OUT_STEP={out_step}")
        print(f"OUT_STL={out_stl}")
        print(f"LINEAR_DEFL={lin_defl}")
        doc, wires = load_wires_from_dxf(dxf)
        print(f"Loaded {len(wires)} closed wires")
        solid = build_solid_from_wires(wires, height)
        print("Built solid; exporting...")
        export_step_and_stl(solid, out_step, out_stl, lin_defl)
        print("Done.")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    main()
