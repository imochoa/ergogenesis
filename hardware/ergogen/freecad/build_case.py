# FreeCAD headless script: build full case (base + walls + standoffs - holes - cutouts)
# Usage:
#   FreeCADCmd -c build_case.py -- \
#     <dxf_dir> <bottom_plate_thickness> <standoff_height> <wall_height> \
#     <out_step> [out_stl] [linear_deflection]
#
# Expects these DXFs in <dxf_dir> (exported from ergogen/config.yaml outlines):
#   - case_base_ol.dxf           (board outline minus screw holes)
#   - wall_ring_ol.dxf           (outer ring minus board outline)
#   - standoff_ol.dxf            (circles at screw positions)
#   - holes_ol.dxf               (screw through-holes)
#   - switch_wall_cutout_ol.dxf  (rect cutout through wall for power switch)
#   - usb_wall_cutout_ol.dxf     (rect cutout through wall for USB-C)

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

from typing import Optional


def log(msg: str):
    sys.stdout.write(msg + "\n")
    sys.stdout.flush()


def load_wires(path: str):
    doc = App.newDocument(os.path.basename(path))
    Import.insert(path, doc.Name)
    doc.recompute()
    wires = []
    for obj in doc.Objects:
        shape = getattr(obj, "Shape", None)
        if not shape:
            continue
        for w in shape.Wires:
            if w.isClosed():
                wires.append(w)
    if not wires:
        raise RuntimeError(f"No closed wires in {path}")
    return wires


def extrude_union(dxf_path: str, height: float) -> Part.Shape:
    wires = load_wires(dxf_path)
    vec = App.Vector(0, 0, float(height))
    solids = []
    for w in wires:
        try:
            face = Part.Face(w)
            solids.append(face.extrude(vec))
        except Exception:
            pass
    if not solids:
        raise RuntimeError(f"No solids extruded from {dxf_path}")
    # Fuse all parts into one
    result = solids[0]
    for s in solids[1:]:
        try:
            result = result.fuse(s)
        except Exception:
            pass
    try:
        result = result.removeSplitter()
    except Exception:
        pass
    return result


def extrude_union_optional(dxf_path: str, height: float) -> Optional[Part.Shape]:
    if not os.path.exists(dxf_path):
        log(f"(optional) missing: {dxf_path}")
        return None
    return extrude_union(dxf_path, height)


def export_step_and_stl(shape, step_path: str, stl_path: Optional[str], lin_defl: float):
    doc = App.newDocument("EXP")
    obj = doc.addObject("Part::Feature", "Case")
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
    if "--" in sys.argv:
        argv = sys.argv[sys.argv.index("--") + 1 :]
    elif "--pass" in sys.argv:
        i = sys.argv.index("--pass")
        argv = sys.argv[i + 1 :]
    else:
        argv = sys.argv[1:]

    if len(argv) < 6:
        sys.stderr.write(
            "Usage: FreeCADCmd build_case.py --pass <dxf_dir> <bottom_th> <standoff_h> <wall_h> <out.step> [out.stl] [lin_defl]\n"
        )
        sys.exit(1)

    dxf_dir = os.path.abspath(argv[0])
    bottom_th = float(argv[1])
    standoff_h = float(argv[2])
    wall_h = float(argv[3])
    out_step = os.path.abspath(argv[4])
    out_stl = os.path.abspath(argv[5]) if len(argv) >= 6 and argv[5] else None
    lin_defl = float(argv[6]) if len(argv) >= 7 else 0.05

    case_base_dxf = os.path.join(dxf_dir, "case_base_ol.dxf")
    wall_ring_dxf = os.path.join(dxf_dir, "wall_ring_ol.dxf")
    standoff_dxf = os.path.join(dxf_dir, "standoff_ol.dxf")
    holes_dxf = os.path.join(dxf_dir, "holes_ol.dxf")
    switch_cut_dxf = os.path.join(dxf_dir, "switch_wall_cutout_ol.dxf")
    usb_cut_dxf = os.path.join(dxf_dir, "usb_wall_cutout_ol.dxf")

    full_h = bottom_th + standoff_h + wall_h

    log("Extruding case components...")
    base = extrude_union(case_base_dxf, bottom_th)
    walls = extrude_union(wall_ring_dxf, full_h)
    standoffs = extrude_union(standoff_dxf, bottom_th + standoff_h)

    case = base.fuse(walls)
    case = case.fuse(standoffs)

    # Subtractions: through-holes + wall cutouts
    holes = extrude_union(holes_dxf, full_h)
    case = case.cut(holes)

    sw_cut = extrude_union_optional(switch_cut_dxf, full_h)
    if sw_cut:
        case = case.cut(sw_cut)
    usb_cut = extrude_union_optional(usb_cut_dxf, full_h)
    if usb_cut:
        case = case.cut(usb_cut)

    try:
        case = case.removeSplitter()
    except Exception:
        pass

    export_step_and_stl(case, out_step, out_stl, lin_defl)

    log("Done.")
