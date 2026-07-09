# Capture Back — Lab 011 Blockout-Style Renderer

## What changed

Seeded Lab 011 for a Workbench-generated C64 projected pit renderer.

## What this proves

```text
renderer_intent.json
  → deterministic projection table
  → deterministic pit line segment table
  → generated ASM data
  → verifier-owned evidence
```

## What this does not prove yet

No runnable PRG yet. The next visual milestone adds C64 bitmap setup and edge drawing.

## Verification

```bash
make -C labs/011_goal_language_to_asm_blockout_renderer verify
```

Expected:

```text
OK: projection table and pit line segment geometry verified.
OK: generated renderer ASM contract verified.
```

## Next move

Draw the generated `pit_line_segments` table onscreen in a C64 emulator.


## Gameboard projection preview

Added an SVG preview generated from the same gameboard definition and pit line segment data:

```text
captures/blockout_gameboard_projection.svg
```

This is not the C64 renderer yet.

It is the first visual proof that the gameboard definition projects into a pit-like board with:

```text
top grid
side/depth rails
z-level projections
```

The next renderer milestone is to make the C64 draw these same line segments.


## Milestone 3 — First runnable PRG

Added a first runnable C64 PRG:

```text
dist/blockout_renderer.prg
```

This first PRG is intentionally crude. It uses a character-screen approximation rather than final bitmap line drawing.

The important Workbench evidence is that the PRG is generated from the same governed line data used by the SVG preview:

```text
renderer_intent.json
  -> pit_line_segments.json
  -> SVG preview
  -> blockout_renderer.prg
```

The PRG therefore shows the governed board, not a separately hand-drawn board.

Next renderer milestone:

```text
replace character-cell approximation with bitmap/pixel line drawing
```


## Projection correction — top-down into the pit

Corrected the Lab 011 gameboard view.

The pit is now rendered as a top-down well:

```text
x/y = visible board opening
z = depth into the well
z guide levels = inset rings
side walls = rails from top perimeter toward deepest ring
```

The SVG preview and the first PRG continue to consume the same generated `pit_line_segments`.

This preserves the Workbench evidence chain while correcting the visual model.


## Perspective projection milestone

Added explicit top-down perspective rings.

The visual model is now:

```text
x/y = visible board opening
z = depth into the well
depth_rings = governed perspective/inset table
```

The SVG and PRG are regenerated from the same governed projection data.

This gets the view right before adding polygon/cube rendering.


## Single cube shaded polygon proof

Added a proof artifact for one cube in the perspective pit:

```text
captures/blockout_single_cube_polygon_preview.svg
dist/single_cube_polygon_faces.json
```

This confirms that the Workbench projection can produce shaded polygon faces for a cube.

The next C64 milestone is not to invent more math. It is to convert the generated face quads into bitmap spans and draw them on the C64.


## Solid red shaded cube faces

Updated the single-cube polygon proof to use solid red shaded faces.

This gives a clearer proof that the projection can support shaded cuboid faces before C64 bitmap/span rendering.


## Single cube polygon spans

Added generated horizontal spans for the red shaded cube.

Artifacts:

```text
dist/single_cube_polygon_spans.json
src/generated_single_cube_spans.s
```

This confirms the next rendering boundary:

```text
solid red cube faces
  -> generated spans
  -> next: C64 bitmap fill rows
```


## C64 bitmap/span-fill PRG proof

Added a runnable PRG that consumes generated single-cube spans and draws a C64 hi-res bitmap payload.

Artifacts:

```text
dist/single_cube_span_fill.prg
dist/single_cube_span_fill_metadata.json
```

This confirms the renderer path from shaded cube faces to C64 span fill.


## Off-side cube in perspective pit

Moved the red shaded cube off-center and added a pit-context SVG.

The C64 span-fill PRG now draws pit wireframe context plus the filled cube spans.

Artifacts:

```text
captures/blockout_pit_with_red_cube.svg
dist/single_cube_span_fill.prg
```


## Same-depth moving cube payload

Generated multiple same-depth cube positions across the pit.

This confirms that movement can be represented as a small set of generated span payloads rather than runtime C64 projection math.

---

## Active white-wireframe correction

The active piece has been corrected from filled red/solid rendering to white wireframe rendering. Colored fill remains a future locked-block behavior only.


---

## Full-height pit and movement crash rule

The pit should be projected into a left playfield that fills the screen top-to-bottom, with a right-side HUD reserved for score/status.

Movement-down causing a blue-screen/broken VIC display is not acceptable visual noise; it is a hard frame-index or pointer bug. For the active 2x1 proof, legal frame index is `y * 4 + x`, range `0..19`.

---

## Pit-only tuning mode

Active-piece rendering was temporarily disabled so the pit projection can be evaluated by itself: depth spacing, bottom size, square viewport, and boundary grid guides.


---

## Pit rules and source contract capture

The pit contract is now explicit in the LI.

Current accepted direction:

```text
5 x 5 x 10 pit
square 196px near viewport
72px far/bottom square
selected visible rings: 0,1,2,3,4,5,6,8,10
all boundary wall grid divisions
no top-plane clutter
compact pit byte records
VIC bank 1: screen $4400, bitmap $6000
```

Compilation model:

```text
LI governs
renderer source spec is machine-readable source
generator emits records / ASM / PRG
PRG is generated artifact
```


---

## Four-cube piece-set capture

The piece source now defines the starter set with a 4-cube maximum.

```text
1..4 cubes
face-contiguous only
max axis extent 3
no 3x3 footprint rotation
```

Pieces are source shapes only; active placement remains separate.


---

## Pose and rotation rules capture

Added pose/rotation source rules.

```text
shape is local cube occupancy
rotation is precomputed normalized occupancy
pose is pieceId + rotationId + x/y/z
```

Rotation candidates are rejected if the rotated piece would leave the pit. Future collision checks will reject rotations that overlap locked blocks.

