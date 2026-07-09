# Lab 011 — Goal Language to ASM: Blockout-Style Polygon Renderer

## Status

Seed LI.

This lab explores whether Workbench can turn declarative geometric intent into deterministic Commodore 64 6502 assembly that renders a constrained 3D-ish game surface.

The visual inspiration is a historical falling-block 3D pit game style. The lab must not copy protected assets, names, exact screen layouts, sprites, logos, game code, or proprietary implementation details.

## Thesis

Lab 010 proves:

```text
goal language → deterministic 6502 movement behavior
```

Lab 011 tests:

```text
geometry intent → projection tables → generated ASM → visual C64 artifact
```

The target is not a general 3D engine.

The target is a constrained renderer:

```text
fixed 3D grid
fixed camera
fixed projection
table-driven coordinates
wireframe pit
projected cuboids
optional filled convex faces later
precomputed piece orientations later
deterministic ASM output
verifier-owned geometry evidence
```

## Boundary

Workbench owns:

```text
intent
generation
generated ASM
verification
capture
```

The C64 runtime consumes generated tables and routines. It should not silently own high-level geometry.

## First milestones

1. Lab shell.
2. Intent JSON.
3. Generated projection table.
4. Generated pit line segment table.
5. Verifiers.
6. Later: bitmap setup and visible wireframe pit.

## Working mantra

```text
Do not make the C64 think harder than necessary.

Make Workbench precompute the geometry.
Make assembly draw the geometry.
Make the verifier prove the contract.
Make the emulator show the artifact.
```


---

## Projection correction — top-down into the pit

Lab 011 uses a top-down pit view.

The player is looking down into the gameboard, not at the pit from the side.

This means:

```text
x/y define the visible board opening
z represents depth into the well
deeper z levels are drawn as inset rings toward the center
side walls are implied by rails connecting corresponding perimeter points
```

The projection source of truth is still:

```text
labs/011_goal_language_to_asm_blockout_renderer/goal/renderer_intent.json
```

The SVG and the C64 PRG are both derived from the generated `pit_line_segments`.

The current SVG/PRG view is intentionally a top-down wireframe proof, not final Blockout-quality bitmap graphics.


---

## Explicit perspective ring projection

The top-down pit projection is governed by an explicit perspective ring table.

This replaces vague perspective math with inspectable data:

```text
z=0   largest opening ring
z=3   smaller guide ring
z=6   smaller guide ring
z=9   smaller guide ring
z=12  deepest visible guide ring
```

The intent carries ring dimensions directly. The generator interpolates between rings when it needs intermediate z coordinates.

The C64 does not calculate perspective.

Workbench precomputes:

```text
depth_rings
  -> projection_table
  -> pit_line_segments
  -> SVG preview
  -> first PRG character-rendering approximation
```

This is the projection boundary before polygon/cuboid rendering begins.


---

## Single cube polygon proof

Before implementing C64 bitmap/span fill, Lab 011 confirms that a single cube in the perspective pit can be decomposed into shaded polygon faces.

The proof artifact is:

```text
captures/blockout_single_cube_polygon_preview.svg
```

The generated polygon data is:

```text
dist/single_cube_polygon_faces.json
```

This confirms:

```text
cube cell + z depth
  -> projected vertices
  -> face quads
  -> shaded polygon preview
```

The C64 does not yet fill these polygons. The next renderer milestone is to convert these face quads into C64 bitmap spans.


---

## Solid red shaded cube proof

Lab 011 now includes a deliberately visible single-cube proof using solid red shaded faces.

Artifacts:

```text
captures/blockout_single_cube_polygon_preview.svg
captures/blockout_single_cube_red_shaded_faces.svg
dist/single_cube_polygon_faces.json
```

The red cube proof confirms:

```text
perspective pit projection
  -> projected cube vertices
  -> five face quads
  -> solid shaded visual faces
```

This is still an SVG/polygon proof, not final C64 bitmap span fill.


---

## C64-facing cube span generation

Lab 011 now generates horizontal span rows from the solid red cube face quads.

Artifacts:

```text
dist/single_cube_polygon_spans.json
src/generated_single_cube_spans.s
```

This is the bridge from polygon proof to C64 bitmap fill:

```text
projected face quads
  -> horizontal spans
  -> C64 fill rows
```

The C64 should not calculate polygon intersections. Workbench generates the span data; the C64 renderer consumes it.


---

## C64 bitmap/span-fill PRG proof

Lab 011 now builds a C64 PRG from the generated cube spans.

Artifacts:

```text
dist/single_cube_span_fill.prg
dist/single_cube_span_fill_metadata.json
```

This milestone proves:

```text
solid red cube faces
  -> generated horizontal spans
  -> C64 bitmap payload
  -> runnable PRG
```

The C64 still does not calculate perspective or polygon intersections. It consumes generated span-fill data.


---

## Off-side cube in perspective pit

The cube proof now places the cube off-center in the pit so the perspective position and side faces are easier to read.

New context artifact:

```text
captures/blockout_pit_with_red_cube.svg
```

The span-fill PRG now includes both:

```text
pit wireframe context
solid red cube spans
```

This confirms the renderer path as a visible object in the pit, not only as an isolated cube.


---

## Same-depth moving cube span payload

Lab 011 now generates multiple same-depth cube positions across the pit.

Artifacts:

```text
captures/blockout_moving_cube_same_depth_preview.svg
dist/moving_cube_same_depth_frames.json
src/generated_moving_cube_spans.s
```

This tests the realtime boundary without asking the C64 to solve projection or polygon intersections:

```text
same z/depth cube positions
  -> precomputed face spans per position
  -> C64 consumes selected frame span payload
```

The initial conservative estimate is span-fill only, not the full game loop.


---

## Byte-span realtime boundary

The naive moving-cube pixel estimate is too slow. The optimized boundary is now byte/mask spans:

```text
pixel span -> C64 bitmap byte offset + mask -> byte write payload
```

Artifacts:

```text
dist/moving_cube_same_depth_byte_spans.json
src/generated_moving_cube_byte_spans.s
```


---

## Moving cube byte-span animation PRG

Lab 011 now builds a C64 PRG that cycles through same-depth cube positions using generated byte/mask span records.

Artifacts:

```text
dist/moving_cube_byte_span_animation.prg
dist/moving_cube_byte_span_animation_metadata.json
```

This proves emulator-visible cube movement using the optimized byte-span runtime boundary.


---

## WASD 5x5 fixed-depth grid control PRG

Lab 011 now builds an interactive C64 proof where the red cube can move to every cell of the 5x5 grid at one depth level.

```text
A/D change x
W/S change y
SPACE returns to center
```

Artifacts:

```text
dist/wasd_5x5_cube_control.prg
dist/wasd_5x5_cube_control_metadata.json
```

This is still precomputed-frame control: 25 generated byte-span draw routines, one for each grid cell.

---

## Active white-wireframe PRG replacement

The active WASD 5x5 proof now removes moving red/solid rendering. The player-controlled piece is generated as compact white wireframe edge records only. Red/solid/color fill is reserved for locked landed blocks and must not be used for the active piece.

---

## Option B green tunnel / white active piece

The active-piece proof uses the Blockout-style target:

```text
pit:
  green-ish wireframe tunnel/grid
  stable background

active_piece:
  white wireframe
  drawn over the pit
  touched 8x8 cells may turn white because C64 hi-res color is cell-based

locked_blocks:
  colored fill later
```

---

## Clean tunnel pit filter

Option B keeps the green pit tunnel, but removes top-plane clutter.

```text
keep:
  outer rim
  inner depth rings
  boundary wall/depth lines

drop:
  top-plane internal helper lines
  top-plane radial/diagonal guide clutter across the opening
```

The active piece remains white wireframe. Locked blocks remain future colored fill.

---

## Active 2x1 piece extent rule

The active proof now uses a 2x1 white-wireframe piece.

```text
piece: 2x1
pit: 5x5
legal x: 0..3
legal y: 0..4
```

Movement must keep the entire rotated footprint inside the pit. Future rotation support must recompute the footprint extent before accepting a rotation. For example, a 2x1 piece rotated 90 degrees becomes 1x2, changing legal bounds to x=0..4 and y=0..3.


---

## Screen layout: full-height pit plus right HUD

The Blockout proof should use the C64 screen as a composed game surface, not as a small centered diagram.

Target screen:

```text
C64 bitmap:
  320 x 200 pixels

playfield / pit:
  left side
  approximately 256 x 200 pixels
  maximize top-to-bottom extent
  top rim near y = 8..12
  bottom/far pit extent near y = 188..194

right HUD:
  approximately 64 x 200 pixels
  reserved for scoring/status
```

Right-side HUD candidates:

```text
score
level
depth
piece count
next piece preview
debug x/y/z/rotation during lab mode
```

The projected pit should be re-fit to the playfield rectangle, not the full 320-pixel width.

```text
projection viewport:
  x_min = 0..8
  x_max = 248..256
  y_min = 8..12
  y_max = 188..194

HUD viewport:
  x_min = 256
  x_max = 319
```

This gives the pit the maximum vertical presence while preserving a stable scoring/status area on the right.

## Movement crash rule

Movement that causes a blue-screen/reset or broken VIC display is a hard renderer bug.

For the current 2x1 active piece:

```text
pit: 5x5
piece: 2x1
legal x: 0..3
legal y: 0..4
legal frame index: y * 4 + x
legal frame index range: 0..19
```

The renderer must reject any move that would produce an index outside the legal frame table.

```text
candidate x/y
  -> check x_min/x_max/y_min/y_max
  -> compute frame index
  -> assert index <= last frame
  -> draw
```

Down movement must clamp/reject at y=4 and must never select frame 20 or beyond.

Future rotation extent rule:

```text
rotation 0:
  footprint 2x1
  legal x 0..3
  legal y 0..4
  index stride 4

rotation 90:
  footprint 1x2
  legal x 0..4
  legal y 0..3
  index stride 5
```

A rotation-aware renderer must compute the frame table stride from the active rotation extent. It must not reuse the unrotated stride blindly.

---

## Runtime correction: full-height projection and fail-closed movement

The 2x1 WASD proof renders the pit in a left full-height playfield and reserves the right side for HUD/scoring.

```text
playfield: x 8..250, y 10..192
HUD reserve: x 256..319
```

The movement runtime fails closed:

```text
clamp x/y before computing frame index
compute index = y * 4 + x
legal index = 0..19
if dispatch misses, reset to center and redraw
```

Moving down at the bottom must not select a missing frame or corrupt the VIC display.

---

## Square pit viewport correction

The pit should not be stretched wider than tall. The C64 screen may reserve a right-side HUD, but the pit projection viewport itself must remain square.

```text
pit viewport:
  square
  x = 36..218
  y = 10..192
  size = 182 x 182

HUD reserve:
  x = 256..319
```

This keeps the pit maximized vertically while preserving square pit geometry.

---

## Maximum square pit height

The pit projection should use as much of the C64 bitmap height as practical while remaining square and preserving the right HUD reserve.

```text
C64 bitmap height: 200 px
safe maximum square pit:
  y = 2..198
  x = 30..226
  size = 196 x 196

HUD reserve:
  x = 256..319
```

This supersedes the earlier 182x182 square viewport. The earlier viewport was square, but not maximized vertically.

---

## Blockout-style 5x5x12 pit visual

The pit visual target is a Blockout-like 5x5x12 tunnel.

```text
pit footprint: 5 x 5
visual depth: 12 rings/layers
near/top square: 196 x 196 px
far/bottom square: 96 x 96 px
HUD reserve: right side
```

The far/bottom square should be large enough to read as a playable bottom, not a tiny pinhole. The tunnel should show more depth layers while avoiding top-plane clutter across the opening.

---

## Pit-only tuning mode

While the pit projection is being tuned, active-piece rendering should be disabled.

```text
pit-only tuning:
  draw pit grid only
  no active piece overlay
  no white touched cells
  no locked blocks
```

Reason:

```text
The pit geometry, depth spacing, bottom square size, and boundary grid guides need to be judged without active-piece/color-cell noise.
```

After the pit is accepted, re-enable the 2x1 active white-wireframe piece.

---

## Pit compact payload optimization

Pit-only tuning should not ship a full bitmap background.

```text
old payload:
  8000-byte pit bitmap source
  1000-byte screen source
  1000-byte color source

new payload:
  compact nonzero pit bitmap byte records
  screen/color generated by C64 startup loops
  bitmap cleared by C64 startup loop
```

The pit is drawn once at startup from compact records. Later, when active pieces return, the same static pit can become the background layer for dirty-byte restoration.


---

## Accepted pit visual and rendering contract

The current accepted pit direction is a **pit-only optimized static background**. Active-piece drawing is intentionally paused until the pit contract is stable.

### Pit geometry

```text
pit footprint:
  width = 5
  height = 5

pit depth:
  depth = 10 playable depth bands
  visible ring domain = z 0..10
```

### Projection viewport

```text
C64 bitmap:
  320 x 200

pit viewport:
  square
  x = 30..226
  y = 2..198
  near/top square = 196 x 196 px
  far/bottom square = 72 x 72 px

right HUD reserve:
  x = 256..319
```

The pit must stay square. The screen may reserve a right-side HUD, but the pit projection itself must not be stretched wider than tall.

### Depth spacing

The pit uses a gameplay-biased depth table, not physically strict camera projection.

```text
depth bands:
  10

possible rings:
  z = 0..10

depth t table:
  z:  0    1    2    3    4    5    6    7    8    9    10
  t: .00  .34  .56  .71  .81  .88  .93  .96  .98  .99  1.00
```

The near/viewer rows receive more visible space. Far/bottom rows compress strongly.

### Visible rings

To avoid a dense pile of rectangles near the far/bottom opening, not every possible ring is drawn.

```text
draw rings:
  z = 0, 1, 2, 3, 4, 5, 6, 8, 10

skip rings:
  z = 7, 9
```

This preserves true depth 10 while reducing visual clutter.

### Wall grid guides

The pit must show all 5 columns/rows around the walls.

```text
front wall boundary guides:
  x = 0..5 at y = 0

back wall boundary guides:
  x = 0..5 at y = 5

left wall boundary guides:
  y = 0..5 at x = 0

right wall boundary guides:
  y = 0..5 at x = 5
```

These guides are continuous from z=0 to z=10.

### Top-plane clutter rule

Do not draw top-plane helper grid lines across the opening.

```text
allowed:
  square rings
  boundary wall grid guides
  straight depth guides

not allowed:
  top-plane helper lattice across the opening
  radial/diagonal clutter not tied to wall boundaries
```

### Line discipline

The projection is gameplay-biased but line-disciplined.

```text
required:
  square centered rings
  straight ring edges
  straight wall/depth guide lines

not required:
  physically strict camera projection
```

## C64 rendering and payload contract

The accepted pit-only runtime uses compact pit byte records rather than a full bitmap source payload.

### Old payload model

```text
full pit bitmap source:
  8000 bytes

screen source:
  1000 bytes

color source:
  1000 bytes
```

### Accepted compact payload model

```text
startup:
  clear bitmap memory
  fill screen/color memory
  draw compact nonzero pit bitmap byte records once
  idle

payload:
  compact nonzero bitmap byte records
```

### VIC memory layout

```text
VIC bank:
  bank 1 = $4000-$7fff

screen memory:
  $4400

bitmap memory:
  $6000

reason:
  keep bitmap memory away from program and compact record table near $0801
```

### Current rendering state

```text
current:
  pit-only tuning
  active piece disabled
  no locked blocks

later:
  pit remains static background
  active piece returns as dirty-byte overlay
  locked blocks become part of static/landed layer
```

## Source-of-truth pipeline

The LI is not itself the final low-level compiler input. The LI governs the contract.

The source of the generated PRG should be a structured renderer source spec.

```text
LI:
  governs purpose, rules, invariants, accepted visual contract

Blockout renderer source spec:
  machine-readable pit/piece/render contract
  JSON/YAML/goal-language

generator:
  compiles source spec into C64 memory records / ASM / PRG

PRG:
  generated runtime artifact
```

The Python builder is currently acting as both generator and source. That should be split.

### Desired source spec shape

```json
{
  "kind": "blockout_renderer_source",
  "pit": {
    "width": 5,
    "height": 5,
    "depth": 10
  },
  "projection": {
    "viewport": {
      "xMin": 30,
      "xMax": 226,
      "yMin": 2,
      "yMax": 198,
      "square": true
    },
    "nearSquarePx": 196,
    "farSquarePx": 72,
    "depthTByZ": [0.00, 0.34, 0.56, 0.71, 0.81, 0.88, 0.93, 0.96, 0.98, 0.99, 1.00],
    "visibleRingZs": [0, 1, 2, 3, 4, 5, 6, 8, 10],
    "straightDepthGuides": true
  },
  "wallGrid": {
    "drawAllBoundaryDivisions": true,
    "drawTopPlaneHelpers": false
  },
  "c64": {
    "vicBank": 1,
    "screenAddress": "$4400",
    "bitmapAddress": "$6000",
    "payloadStrategy": "compact_nonzero_bitmap_byte_records"
  },
  "renderPriority": [
    "pit",
    "locked_blocks",
    "active_piece"
  ]
}
```

### Compilation direction

```text
LI
  -> renderer source spec
  -> generated pit byte records
  -> generated ASM/PRG
```

The source spec should become the reproducible authority for the PRG. ASM and PRG should remain generated artifacts.


---

## Four-cube piece-set constraint

The first Blockout-style piece set is limited to small contiguous polycubes.

```text
cube count:
  1..4

max extent:
  3 on any axis

footprint rule:
  no rotation may be 3x3 in the pit plane

connectivity:
  all cubes must be face-contiguous
```

The source piece list is:

```text
P01_MONO
  one cube; debug/baseline

P02_DOMINO
  two-cube straight domino

P03_LINE
  three-cube straight line

P03_ELBOW
  three-cube L/corner

P04_SQUARE
  four-cube 2x2 slab

P04_T
  four-cube T

P04_L
  four-cube long L

P04_S
  four-cube zig-zag

P04_CORNER_3D
  four-cube 3D corner with x/y/z arms
```

These are piece-shape definitions only. Placement is separate active-piece state.

```text
shape:
  pieceId + rotationId + local cubes

placement:
  active x/y/z in the pit
```

The renderer must derive exposed outline edges from the occupied cube set and must not draw internal cube-to-cube seams.


---

## Pose and rotation rules

Piece shape is separate from active placement.

```text
piece shape:
  pieceId + local cube set

rotation:
  rotationId + normalized local cube set

pose:
  pieceId + rotationId + x/y/z
```

Rotation is not pixel rotation. Rotation means selecting a precomputed normalized cube occupancy.

```text
candidate rotation:
  select rotationId
  load normalized local cubes
  compute/read extent
  test current x/y/z pose
  reject if any cube would leave pit bounds
  future: reject if any cube would overlap locked occupancy
```

For the C64 proof, runtime should choose among precomputed rotation IDs. It should not do runtime matrix math.

Current first overlay phase:

```text
gravity:
  not implemented

locked-block collision:
  not implemented

z:
  fixed test layer z = 0

movement:
  x/y legal by rotated extent

rotation:
  legal only if current pose still fits the pit
```

Future gameplay phase:

```text
legal pose:
  inside pit bounds
  no locked-block collision

legal rotation:
  rotated world cubes remain inside pit
  rotated world cubes do not collide

landing:
  if next drop pose is illegal, current pose locks
```

Pose rules source:

```text
labs/011_goal_language_to_asm_blockout_renderer/source/blockout_pose_rules.json
```

## Companion LI

- [Active piece payload pipeline](011_goal_language_to_asm_blockout_renderer_active_piece_pipeline.md)
## Companion LI++

- [LI++ lean runtime doctrine](011_goal_language_to_asm_blockout_renderer_li_plus_plus_runtime_doctrine.md)
