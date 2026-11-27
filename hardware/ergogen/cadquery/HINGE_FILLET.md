# Adjustable Tenting Hinge Fillet

## Geometry

The case and floor use complementary cylindrical surfaces along the outer case
edge:

- The case has a 1.0 mm convex radius cut into its bottom outer edge.
- The floor plate adds a fully supported bearing wall with a relieved concave
  inner radius.
- The case rotates around the center of its radius; the floor seat remains
  fixed.
- The floor radius is 0.2 mm larger and is raised by the same amount. This keeps
  the two parts tangent at the bottom while providing clearance along the curved
  flank for FDM variation.

The result is a continuous contact line along the pivot span at every configured
angle. Setting the radial clearance to zero makes the radii nominally identical,
but is likely to bind when printed.

The rotation-center change is included in the case/floor groove calculations.
Changing the pivot radius therefore does not require manually repositioning the
support-card grooves.

## Parameters

The source of truth is the `units` section in `hardware/ergogen/config.yaml`:

| Parameter | Default | Purpose |
| --- | ---: | --- |
| `tenting_pivot_radius` | 1.0 mm | Convex case radius and pivot-axis height |
| `tenting_pivot_radial_clearance` | 0.2 mm | Additional floor-seat radius and flank relief |
| `tenting_edge_clearance` | 0.4 mm | General clearance to the contour guide |
| `tenting_edge_guide_height` | 1.5 mm | Height of the retaining guide |
| `tenting_edge_wall_thickness` | 2.0 mm | Retaining-guide wall thickness |

Keep the pivot radius between 0.8 and 1.2 mm. The case base is 2.4 mm thick, so a
larger radius would leave too little material at the first layers of the wall.
Change one parameter at a time in 0.05-0.1 mm increments.

## Rebuild and inspect

From the repository root:

```bash
just hardware cq-build-adjustable-tenting
```

The command regenerates the Ergogen outlines and writes the case, floor, card,
and angle assemblies to:

```text
hardware/ergogen/output/cases/
```

Inspect these STEP files first:

```text
adjustable_tenting_case_left.step
adjustable_tenting_floor_left.step
adjustable_tenting_10deg_left.step
adjustable_tenting_20deg_left.step
adjustable_tenting_30deg_left.step
```

Run the geometry and slot-position check without exporting files:

```bash
uv run hardware/ergogen/cadquery/build_adjustable_tenting.py inspect \
  --config hardware/ergogen/config.yaml \
  --dxf-dir hardware/ergogen/output/outlines
```

This validates the solids and checks for collisions at every configured angle.

## PLA print test

For a 0.4 mm nozzle, start with:

```text
PLA, 0.12-0.16 mm layers, 3 walls, 20% gyroid, no supports.
Orientation: case and floor flat on their normal bottom faces.
```

The floor's concave bearing surface narrows as it rises and is self-supporting.
The case radius expands outward during its first few layers; a 1.0 mm radius is
small enough to print without supports, but 0.2 mm layers can leave a visibly
stepped contact surface. Use 0.12 mm layers for the first fit test if surface
quality matters.

Enable the slicer's normal elephant-foot compensation. Avoid a brim touching the
pivot edge, since brim removal can damage the radius. Remove any loose first-layer
ridge with a deburring tool before judging the fit.

## Iteration strategy

1. Print one case and one floor plate before producing both halves.
2. Test the case at 10, 20, and 30 degrees without the support card and confirm
   that the pivot rolls without catching.
3. Insert the card and check for sideways play, rocking, and groove alignment.
4. Change only `tenting_pivot_radial_clearance`, rebuild, and repeat.

Use these adjustments:

| Symptom | Adjustment |
| --- | --- |
| Pivot catches or squeaks | Increase radial clearance by 0.05 mm |
| Visible rocking at the pivot | Reduce radial clearance by 0.05 mm |
| First layers are rough | Use 0.12 mm layers and verify elephant-foot compensation |
| Radius chips during removal | Move the brim away from the pivot or omit it |
| Pivot feels too sharp | Increase radius by 0.1 mm, up to 1.2 mm |

A radial clearance of 0.15-0.30 mm is the practical range for PLA. Zero clearance
is useful only as a dimensional calibration test.

## Troubleshooting

If the case and floor collide in the generated assembly, run the `inspect`
command and restore the last known radius/clearance pair before changing other
features. Do not compensate by moving card grooves manually; their positions are
computed from the pivot center.

If a printed fit differs between the left and right halves, first check slicer
orientation and elephant-foot compensation. The right model is mirrored from the
same solid, so a geometry difference is unlikely.
