# FreeCAD headless script: extrude a DXF outline into a solid and export STEP/STL
# Usage (CLI):
#   FreeCADCmd -c extrude_dxf.py -- <input.dxf> <height_mm> <out.step> [out.stl] [linear_deflection]
#
# Notes:
# - Assumes the DXF contains one outer boundary and any number of inner closed
#   loops (holes/cutouts). We build the largest face as the base and subtract
#   all other faces extruded to the same height.
# - Set a smaller linear_deflection for finer STL meshing (default 0.05 mm).

import sys
import os

try:
    import FreeCAD as App
    import Part
    import Import
    import Mesh
    import MeshPart
except Exception as e:
    sys.stderr.write(f"This script must be run by FreeCADCmd: {e}\n")
    sys.exit(2)


def log(msg: str):
    sys.stdout.write(msg + "\n")
    sys.stdout.flush()


def load_wires_from_dxf(path: str):
    doc = App.newDocument("DXF")
    # Import.insert allows specifying destination doc
    Import.insert(path, doc.Name)
    doc.recompute()
    wires = []
    for obj in doc.Objects:
        shape = getattr(obj, "Shape", None)
        if not shape:
            continue
        # Collect all wires contained in the imported shape
        for w in shape.Wires:
            if w.isClosed():
                wires.append(w)
    if not wires:
        raise RuntimeError(f"No closed wires found in {path}")
    return doc, wires


def build_solid_from_wires(wires, height: float):
    # Create faces from wires and identify the outermost by area
    faces = []
    for w in wires:
        try:
            f = Part.Face(w)
            faces.append(f)
        except Exception:
            # Non-planar or invalid wire; skip
            pass
    if not faces:
        raise RuntimeError("No faces could be created from DXF wires")
    faces.sort(key=lambda f: f.Area, reverse=True)
    base_face = faces[0]
    vec = App.Vector(0, 0, float(height))
    solid = base_face.extrude(vec)
    # Subtract all other faces (holes/cutouts)
    for hole_face in faces[1:]:
        try:
            hole_prism = hole_face.extrude(vec)
            solid = solid.cut(hole_prism)
        except Exception:
            # Keep going even if a small hole fails (e.g., degenerate geometry)
            pass
    try:
        solid = solid.removeSplitter()
    except Exception:
        pass
    return solid


def export_step_and_stl(shape, step_path: str, stl_path: str | None, lin_defl: float):
    # Export STEP
    # Wrap in a transient object for exporter convenience
    doc = App.newDocument("EXP")
    obj = doc.addObject("Part::Feature", "Result")
    obj.Shape = shape
    doc.recompute()
    Part.export([obj], step_path)
    log(f"Wrote STEP: {step_path}")

    if stl_path:
        mesh = MeshPart.meshFromShape(
            Shape=shape,
            LinearDeflection=float(lin_defl),
            AngularDeflection=28.5,
            Relative=False,
        )
        mesh.write(stl_path)
        log(f"Wrote STL:  {stl_path}")


if __name__ == "__main__":
    # Accept args via either "--" separator or FreeCAD's "--pass" mechanism.
    argv = []
    if "--" in sys.argv:
        argv = sys.argv[sys.argv.index("--") + 1 :]
    elif "--pass" in sys.argv:
        i = sys.argv.index("--pass")
        argv = sys.argv[i + 1 :]
    else:
        argv = sys.argv[1:]

    if len(argv) < 3:
        sys.stderr.write(
            "Usage: FreeCADCmd extrude_dxf.py --pass <input.dxf> <height_mm> <out.step> [out.stl] [linear_deflection]\n"
        )
        sys.exit(1)

    dxf_path = os.path.abspath(argv[0])
    height = float(argv[1])
    out_step = os.path.abspath(argv[2])
    out_stl = os.path.abspath(argv[3]) if len(argv) >= 4 and argv[3] else None
    lin_defl = float(argv[4]) if len(argv) >= 5 else 0.05

    if not os.path.exists(dxf_path):
        sys.stderr.write(f"DXF not found: {dxf_path}\n")
        sys.exit(1)

    os.makedirs(os.path.dirname(out_step), exist_ok=True)
    if out_stl:
        os.makedirs(os.path.dirname(out_stl), exist_ok=True)

    log(f"Importing DXF: {dxf_path}")
    doc, wires = load_wires_from_dxf(dxf_path)
    log(f"- Closed wires: {len(wires)}")

    log(f"Extruding: height={height} mm")
    solid = build_solid_from_wires(wires, height)

    export_step_and_stl(solid, out_step, out_stl, lin_defl)

    log("Done.")
