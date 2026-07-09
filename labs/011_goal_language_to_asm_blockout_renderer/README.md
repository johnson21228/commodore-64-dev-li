# Lab 011 — Goal Language to ASM: Blockout-Style Polygon Renderer

This lab explores a constrained C64 renderer inspired by classic 3D falling-block pit games.

The goal is not to build a general 3D engine. The goal is to prove a Workbench path:

```text
geometry intent
  → deterministic projection tables
  → generated 6502 assembly
  → verifier-owned evidence
  → runnable C64 visual artifact
```

## Current milestone

This seed creates:

```text
intent JSON
generator
projection table
pit line segment table
renderer ASM contract stub
verifiers
```

It does not yet build a runnable PRG.

## Commands

```bash
make generate
make verify
make build
make run
make clean
```


## Milestone 3 — First runnable PRG

The first runnable PRG uses a character-screen approximation.

It reads the generated `dist/pit_line_segments.json`, maps projected C64 coordinates into 40x25 screen cells, and emits:

```text
dist/blockout_renderer.prg
```

This is intentionally not the final bitmap renderer.

It proves:

```text
governed gameboard definition
  -> generated pit_line_segments
  -> runnable C64 artifact
```


## Top-down pit projection

The board is rendered as a top-down well.

`x` and `y` define the 5x5 board opening. `z` is depth into the pit. Deeper guide levels are inset toward the center.

This corrects the first crude side/oblique view and better matches the intended Blockout-style view.


## Explicit perspective depth rings

The perspective pit is now controlled by explicit ring dimensions in `goal/renderer_intent.json`.

This makes the view inspectable and verifiable before adding cube or polygon rendering.


## Single cube polygon proof

`make polygon-proof` creates a shaded SVG proof of one cube inside the perspective pit.

This confirms the polygon math before C64 bitmap/span rendering.


## Solid red shaded cube faces

The single-cube polygon proof now renders with solid red shaded faces.

Open:

```text
captures/blockout_single_cube_red_shaded_faces.svg
```


## Single cube polygon spans

`make spans` generates horizontal span rows from the single red cube face quads.

These spans are the C64-facing rasterization payload.


## C64 bitmap/span-fill proof

`make span-prg` builds a runnable C64 PRG from the generated red cube spans.

`make run-span-prg` opens the span-fill PRG in VICE when available.


## Off-side cube in pit context

The red cube proof is now placed to one side of the pit.

Open:

```text
captures/blockout_pit_with_red_cube.svg
```

Run:

```text
make run-span-prg
```

to see the C64 bitmap/span-fill proof with pit context.


## Same-depth moving cube

`make moving-cube` generates several same-depth red cube positions and C64-facing span payloads.

Open:

```text
captures/blockout_moving_cube_same_depth_preview.svg
```


## Moving cube byte-span PRG

`make moving-byte-prg` builds a runnable C64 PRG that cycles the cube through same-depth byte-span frames.

`make run-moving-byte-prg` opens it in VICE when available.


## WASD 5x5 grid PRG

`make wasd-grid-prg` builds the interactive 5x5 fixed-depth cube-control PRG.

`make run-wasd-grid-prg` opens it in VICE. Use A/D/W/S and SPACE.

## Active white-wireframe PRG

`make wasd-grid-prg` now builds a white-wireframe active-piece proof. The moving red solid cube path is deprecated for active control.

## Option B green grid / white piece

`make wasd-grid-prg` targets a green-ish pit wireframe tunnel with a white active wireframe piece. Red/solid moving-piece rendering remains removed.

## Clean tunnel pit filter

The Option B WASD proof now filters the pit background to keep the tunnel readable:

```text
green clean tunnel wireframe
white active wireframe piece
no top-plane helper clutter
```

## Active 2x1 piece

`make wasd-grid-prg` now builds a 2x1 white-wireframe active piece. WASD movement is clamped so the full piece stays inside the 5x5 pit. Rotation is not implemented yet; rotation must recompute extent bounds.


## Full-height pit plus right HUD

The Blockout proof should maximize the pit vertically and reserve the right side for scoring/status.

```text
screen: 320x200
pit/playfield: left ~256x200
HUD/scoring: right ~64x200
```

The current 2x1 movement must stay inside its 20 legal states:

```text
x = 0..3
y = 0..4
index = y * 4 + x
index = 0..19
```

Any down movement that breaks the screen is a hard renderer/indexing bug.

## Full-height runtime correction

The active 2x1 WASD proof refits the pit to a left full-height playfield and reserves the right edge for HUD/scoring. Runtime movement is guarded so the 20-state frame table fails closed instead of selecting an invalid frame.

## Square pit viewport correction

The pit projection is square inside the left playfield:

```text
x = 36..218
y = 10..192
size = 182 x 182
```

The right side remains reserved for HUD/scoring.

## Maximum square pit height

The pit projection now uses a near-full-height square viewport:

```text
x = 30..226
y = 2..198
size = 196 x 196
```

The right side remains reserved for HUD/scoring.

## Blockout-style 5x5x12 pit visual

The WASD proof now draws a direct 5x5x12 tunnel:

```text
near/top square: 196 x 196
far/bottom square: 96 x 96
visible depth rings: 12
```

The active piece remains a 2x1 white wireframe block.

## Pit-only tuning mode

`make wasd-grid-prg` currently builds a pit-only projection tuning proof. The active 2x1 piece is disabled until the pit projection is accepted.

## Pit compact payload optimization

The pit-only PRG now uses compact nonzero bitmap byte records instead of embedding a full 8000-byte pit bitmap plus 2000 bytes of screen/color source.


## Pit rendering contract and source pipeline

The current accepted pit proof is:

```text
pit: 5 x 5 x 10
viewport: square, x=30..226, y=2..198
near square: 196 x 196
far square: 72 x 72
visible rings: 0,1,2,3,4,5,6,8,10
wall guides: all 5x5 boundary divisions on all four walls
top-plane clutter: none
VIC bank: 1
screen: $4400
bitmap: $6000
payload: compact nonzero bitmap byte records
```

The LI governs the rules, but the PRG should compile from a structured renderer source spec. The Python builder is currently acting as both source and generator; the next architectural step is to split those roles.


## Four-cube starter piece set

The piece source now limits pieces to 1..4 face-contiguous cubes.

```text
P01_MONO
P02_DOMINO
P03_LINE
P03_ELBOW
P04_SQUARE
P04_T
P04_L
P04_S
P04_CORNER_3D
```

No rotation may exceed extent 3 on any axis, and no rotation may occupy a 3x3 footprint in the pit plane.


## Pose and rotation rules

Pose rules are now source data:

```text
source/blockout_pose_rules.json
tools/verify_blockout_pose_rules.py
```

A pose is:

```text
pieceId + rotationId + x/y/z
```

Rotation is selected from precomputed normalized cube occupancies. The C64 runtime should not do matrix rotation math.

## Active piece payload pipeline

Lab 011 defines an active-piece / locked-occupancy boundary:

- active pieces are dynamic white outlined pieces only;
- locking expands the active piece into occupied cells and discards the piece instance;
- locked occupancy is cell-first, not locked-piece-first;
- per-piece payloads are generated offline and only the current payload is loaded/copied into the active runtime slot;
- sprites may support HUD/effects, but the main active piece remains bitmap dirty-overlay rendered.

See:

- `captures/CAPTURE_BACK_ACTIVE_PIECE_PIPELINE_AND_LOCKED_OCCUPANCY.md`
- `source/blockout_runtime_pipeline_contract.json`
- `tools/verify_blockout_runtime_pipeline_contract.py`

## LI++ lean runtime doctrine

Lab 011 captures a lean-runtime doctrine:

- the intelligence lives upstream;
- the runtime stays lean;
- the payload is the contract;
- the screen is the proof;
- the C64 executes current payload records instead of reasoning about Blockout geometry.

See:

- `captures/CAPTURE_BACK_LI_PLUS_PLUS_LEAN_RUNTIME_DOCTRINE.md`
- `source/blockout_li_plus_plus_runtime_doctrine.json`
- `tools/verify_blockout_li_plus_plus_runtime_doctrine.py`

## P02_DOMINO payload report

Lab 011 begins the per-piece payload pipeline with a report-only target:

- `P02_DOMINO`
- `x_axis` and `y_axis` rotations only
- all legal `x/y/z` poses
- no `z_axis`
- no runtime drawing
- no binary payload yet

Generated artifacts:

- `dist/pieces/P02_DOMINO.payload_report.json`
- `dist/pieces_manifest.json`

Verifier:

- `tools/verify_blockout_p02_domino_payload_report.py`

## P02_DOMINO endpoint payload report

The raw byte/mask payload report was too large for the lean active-payload model.

The endpoint/topology report compares:

- projected endpoint segment records;
- grid-reference records;
- the prior raw byte/mask estimate.

Generated artifact:

- `dist/pieces/P02_DOMINO.endpoint_payload_report.json`

Verifier:

- `tools/verify_blockout_p02_domino_endpoint_payload_report.py`

## P02_DOMINO top-level endpoint preview

The first endpoint/topology visual proof draws a single dynamic block pose:

- `P02_DOMINO`
- `x_axis`
- `x=1, y=2, z=0`
- top level
- white outline over the green pit
- preview only, no movement or dirty restore yet

Build:

```bash
python3 labs/011_goal_language_to_asm_blockout_renderer/tools/build_p02_domino_top_endpoint_preview_prg.py
python3 labs/011_goal_language_to_asm_blockout_renderer/tools/verify_p02_domino_top_endpoint_preview_prg.py
```

## P02_DOMINO white dashed pit preview

This preview tests a C64-native line-style distinction:

- pit: white subtle dashed lines;
- dynamic block: solid white outline;
- background: black.

Build:

```bash
python3 labs/011_goal_language_to_asm_blockout_renderer/tools/build_p02_domino_white_dashed_pit_preview_prg.py
python3 labs/011_goal_language_to_asm_blockout_renderer/tools/verify_p02_domino_white_dashed_pit_preview_prg.py
```

## P02_DOMINO full rotation keys preview

This preview adds original-game-style rotation keys for the dynamic block:

- `A` / `Q`: x-axis orientation;
- `S` / `W`: y-axis orientation;
- `D` / `E`: z-axis orientation.

It is an ASAP interactive proof. It uses the dashed-white pit and solid-white dynamic block line grammar.

Build:

```bash
python3 labs/011_goal_language_to_asm_blockout_renderer/tools/build_p02_domino_full_rotation_keys_preview_prg.py
python3 labs/011_goal_language_to_asm_blockout_renderer/tools/verify_p02_domino_full_rotation_keys_preview_prg.py
```
