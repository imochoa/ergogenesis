# CadQuery path — learnings and notes

This document records what we learned while adding a CadQuery-based pipeline to
generate STEP/STL for the plates and full case directly from Ergogen DXFs, and
then verifying geometry parity against the existing JSCAD meshes.

## Why CadQuery

- FreeCAD CLI is capable but finicky for headless scripting (argument passing,
  module pathing, exporter behavior). We had trouble invoking our scripts
  reliably via `freecadcmd -c` and getting writes to land.
- CadQuery exposes a clean Python API on top of OCP/OpenCascade and runs as a
  normal Python process. With uv single-file scripts we get reproducible,
  dependency-isolated CLIs that are easy to call from `just`.

## Source geometry (DXFs)

All solids are built exclusively from outlines exported by Ergogen:

- switch_plate_ol.dxf — PCB outline minus Choc cutouts and screw holes
- bottom_plate_ol.dxf — PCB outline minus socket slots and screw holes
- case_base_ol.dxf — solid base (board outline minus screw holes)
- wall_ring_ol.dxf — outer perimeter ring (expanded outline minus board outline)
- standoff_ol.dxf — circles at screw positions (standoffs)
- holes_ol.dxf — screw through-holes
- switch_wall_cutout_ol.dxf — rectangle through the case wall for power switch
- usb_wall_cutout_ol.dxf — rectangle through the north wall for USB-C

Note: a few of these outlines were added to `config.yaml` specifically to make a
reliable case reconstruction possible in external CAD.

## Scripts (uv single-file CLIs)

- cadquery/extrude_dxf.py
  - Input: one DXF outline
  - Builds faces from closed wires, extrudes to a prism; if multiple wires are
    present, it treats the largest as the outer boundary and the rest as holes.
  - Output: STEP (+ optional STL)
  - Usage example:
    - uv run cadquery/extrude_dxf.py \
      --dxf ergogen/output/outlines/switch_plate_ol.dxf \
      --height 1.6 \
      --out-step ergogen/output/cases/switch_plate_cq.step \
      --out-stl ergogen/output/cases/switch_plate_cq.stl

- cadquery/build_case.py
  - Inputs: the DXF set listed above (via a directory), plus bottom/standoff
    heights and wall height.
  - Build recipe (all via boolean ops):
    - base = case_base_ol.extrude(bottom_th)
    - walls = wall_ring_ol.extrude(bottom_th + standoff_h + wall_h)
    - standoffs = standoff_ol.extrude(bottom_th + standoff_h)
    - case = base ∪ walls ∪ standoffs
    - holes = holes_ol.extrude(full_height) → case = case − holes
    - switch_cut, usb_cut extruded to full height → subtract from case
  - Output: STEP (+ optional STL)
  - Usage example:
    - uv run cadquery/build_case.py \
      --dxf-dir ergogen/output/outlines \
      --bottom-th 2.0 --standoff-h 2.0 --wall-h 5.0 \
      --out-step ergogen/output/cases/case_cq.step \
      --out-stl ergogen/output/cases/case_cq.stl

## Just recipes

- just hardware cq-build-plates — build switch/bottom plates (STEP+STL)
- just hardware cq-build-case — build the case (STEP+STL)
- just hardware cq-compare — compare CadQuery vs JSCAD meshes
- just hardware cq-iterate — one-shot build-everything-then-compare

These search heights from `ergogen/config.yaml` with ripgrep and write to
`ergogen/output/cases/`.

## Comparison methodology

- Tool: `ergogen/freecad/compare_meshes.py` (uv script using trimesh + scipy + rtree)
- Metrics:
  - Volume difference (absolute and relative %)
  - Surface area difference (absolute)
  - Approximate bidirectional Hausdorff distance (sampling-based)
- Defaults: ≤0.1% volume difference and ≤0.05 mm Hausdorff distance qualify as
  a match. You can pass different tolerances on the CLI if needed.

## Results (with current config)

- Switch plate: ΔV ~0.0033%, Hausdorff ~0.0071 mm (MATCH)
- Bottom plate: ΔV ~0.0024%, Hausdorff ~0.0075 mm (MATCH)
- Case (base+walls+standoffs−holes−cutouts): ΔV ~0.0025%, Hausdorff ~0.0142 mm (MATCH)

These are well within manufacturing tolerances and typical mesh discretization
error.

## API gotchas and fixes

- CadQuery DXF import returns a Workplane, not a Compound. Use:
  - `wp = importers.importDXF(path)`
  - `wires = [w for w in wp.wires().vals() if isinstance(w, cq.Wire) and w.Closed()]`
- Building solids from faces:
  - `cq.Face.makeFromWires(outer, holes)` creates a planar face with holes.
  - Faces don’t have `.extrude()`, so wrap in a Workplane: `cq.Workplane("XY").add(face).extrude(h)`
- Full case needs proper “holes in faces” handling (outer wire + hole wires).
  A naïve “extrude all wires, then subtract” can fail on shared boundaries.
- Export tolerances: CadQuery’s default tessellation was sufficient to match the
  JSCAD meshes within ~0.01 mm; if a future model needs tighter control, we can
  expose tessellation parameters explicitly.

## FreeCAD notes (why we pivoted)

- Argument passing through `freecadcmd` is inconsistent across versions. `--`
  and `--pass` behave differently; reading args and writing files was unreliable
  in our environment.
- Module import path for neighbor modules required extra `sys.path` tweaks.
- We left the FreeCAD scripts in place for reference, but the CadQuery path is
  now the recommended one.

## Dependencies

- uv is used to run the single-file scripts. Install once from Astral if
  missing.
- CadQuery pulls OCP/VTK/Numba/etc.; first run will download a few hundred MB.
- The compare tool depends on trimesh, numpy, scipy, and rtree.

## Future work

- Parameterize STL tessellation for CQ exports if we ever need 1:1 triangle
  parity (currently unnecessary).
- Wrap the CadQuery builds into a single orchestrator script (optional), though
  `just cq-iterate` already provides a good UX.
