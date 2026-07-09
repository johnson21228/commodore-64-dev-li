# Capture Back: Active Piece Pipeline and Locked Occupancy

## Decision

A Blockout `piece` exists only while it is active/dynamic.

Active pieces are:

- white outlined;
- movable;
- rotatable;
- drop-able;
- rendered through active dirty overlay records.

When a piece locks, it does **not** become a locked piece. Locking expands the active piece at its final pose into occupied cells. The active piece object is then discarded.

```text
piece source definition
        ↓
active piece instance
        ↓ locks
occupied cells
        ↓
static locked layer rendering
```

## Runtime lifecycle

```text
spawn:
  choose pieceId
  pull/load/copy that piece payload into ACTIVE_PIECE_TABLE
  set spawn rotationId and x/y/z
  draw white outlined active piece

move/rotate/drop:
  restore previous active dirty region from the static layer
  compute candidate pose key
  check pit bounds and locked occupancy
  if legal, select candidate pose record
  draw active wireframe records
  remember current dirty pointer

lock:
  restore/remove active overlay
  expand active piece + rotation + pose into occupied cells
  write those cells to lockedOccupancy
  rebuild or update static layer
  discard active piece instance
  spawn next active piece
```

## Source pipeline

```text
LI / design contract
        ↓
source/blockout_piece_source.json
source/blockout_pose_rules.json
source/blockout_pit_source.json
source/blockout_runtime_pipeline_contract.json
        ↓
generator
        ↓
dist/blockout_runtime.prg
dist/pieces/<pieceId>.bin
dist/pieces_manifest.json
        ↓
runtime loads one current piece payload
```

## Generated/offline responsibilities

The host-side generator may compute:

- piece rotations;
- legal pose tables;
- pose occupied cells;
- exposed active outline edges;
- projection;
- line rasterization;
- bitmap byte offsets;
- bitmap masks;
- dirty bitmap offsets;
- touched 8x8 color cells;
- per-piece compact payload files;
- payload size reports.

## Runtime responsibilities

The C64 runtime should only do small state work:

- hold one active piece payload at a time;
- track current active pose;
- remember previous dirty pointer;
- calculate candidate x/y/z or rotationId;
- reject candidates that violate bounds or collide with locked occupancy;
- restore previous dirty bytes from the static layer;
- draw current active byte/mask records;
- lock active cubes into occupied cells.

## Runtime non-goals

The C64 runtime should not perform:

- 3D rotation matrix math;
- projection math;
- active-piece line rasterization;
- bitmap mask discovery;
- all-shapes resident payload storage.

## Piece payload file I/O direction

The runtime should be built around one active piece payload at a time.

```text
resident runtime:
  pit/static renderer
  input loop
  locked occupancy
  active-piece slot
  payload loader/copy routine

piece data files:
  one compact payload per piece family
```

Early proof may embed one payload while preserving the same binary contract:

```text
Stage 1:
  piece payload embedded but formatted like a file

Stage 2:
  payload copied into ACTIVE_PIECE_TABLE

Stage 3:
  payload loaded from disk/file into ACTIVE_PIECE_TABLE
```

## Locked occupancy model

Locked blocks are not locked pieces.

After lock, gameplay authority is the cell grid:

```text
lockedOccupancy[x][y][z] = occupied / color
```

Optional provenance may remain for debug/replay/color identity:

```text
cell.sourcePieceId
cell.pieceInstanceId
```

But collision, layer clearing, shifting, and locked rendering use occupied cells, not piece objects.

## Rendering layers

```text
pit layer:
  permanent green tunnel/grid

locked layer:
  solid/color occupied cells
  changes only when pieces lock or layers clear

active layer:
  temporary white wireframe piece
  restored/redrawn every movement
```

The static layer is:

```text
static = pit + locked occupancy rendering
```

Active dirty restore restores from the current static layer.

## Locked block rendering

Locked rendering should operate on the whole occupied-cell set, not on landed pieces independently.

```text
for each locked occupied cell:
  for each face:
    if neighboring cell is empty:
      face is exposed
    else:
      face is internal
```

This avoids internal clutter when cells from different source pieces touch.

## Layer clear and downward movement

With `z` increasing downward:

```text
clear completed layer zc
remove all cells where z == zc
for all occupied cells where z < zc:
  z = z + 1
```

Cells beyond the pit depth are out of view and removed from logical occupancy.

## Sprite policy

Sprites may be used for support effects:

- next-piece preview;
- cursor/origin marker;
- lock flash;
- HUD rotation hint.

Sprites are not the primary falling-piece renderer. The main active piece remains bitmap-rendered from piece + pose dirty records.

## Architectural rule

```text
Precompute per-piece payloads offline.
Load or copy only the current piece payload into the active runtime slot.
Active pieces are dynamic white outlines.
Locking transfers piece cubes into occupied cells.
The piece then goes away.
Locked occupancy renders into the static layer.
```
