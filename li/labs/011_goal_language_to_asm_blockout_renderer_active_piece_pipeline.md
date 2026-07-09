# Lab 011 LI: Active Piece Payload Pipeline

## Intent

Define the durable source and runtime boundary for the C64 Blockout renderer.

The lab should not grow toward one giant resident table containing every possible shape. It should grow toward a runtime that pulls one prepared piece payload at a time, draws it as a dynamic white active piece, and transfers it into locked occupied cells when it lands.

## Core distinction

```text
Active piece:
  dynamic white outline
  pieceId + rotationId + x/y/z
  uses active dirty overlay records
  can move, rotate, and drop

Locked occupancy:
  static colored occupied cells
  no longer pieces
  used for collision, layer clear, downward shift, and locked rendering
```

A piece does not become a locked piece. It disappears as a piece when it locks. Its cubes become occupied cells.

## Source pipeline

```text
LI / design contract
        ↓
structured JSON source
        ↓
per-piece payload generator
        ↓
runtime PRG + piece payload files
        ↓
runtime loads one current piece payload
```

## Runtime boundary

The C64 runtime selects records; it does not derive visual geometry.

Runtime should not compute projection, line rasterization, bitmap masks, or all-shapes pose tables.

## File I/O direction

The design target is one compact payload file per piece family.

```text
ACTIVE_PIECE_TABLE:
  current loaded piece payload only
```

The first proof may embed the payload while preserving the same payload contract. This keeps the architecture file-I/O-ready without forcing disk loading into the first dirty-rendering proof.

## Locked occupancy rule

Locked occupancy is cell-first.

```text
lockedOccupancy[x][y][z] = {
  occupied,
  color,
  optional sourcePieceId,
  optional pieceInstanceId
}
```

Optional source fields are provenance, not gameplay authority.

Collision, layer completion, downward shift, and rendering use cells.

## Rendering rule

```text
static layer = pit + locked occupied cells
active layer = temporary white wireframe overlay
```

Active dirty restore must restore from the current static layer, not from the original pit-only background.

When a piece locks or a layer clears, the active overlay must first be absent. Then occupancy mutates, static rendering updates, and the next active piece is drawn.

## Sprite rule

Sprites are allowed for secondary surfaces and effects only. The active falling piece remains bitmap-rendered from generated dirty records.
