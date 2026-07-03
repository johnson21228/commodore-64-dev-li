# Lab 010 — Sprite Projection Contract

## Purpose

This note records the coordinate boundary for Lab 010 Pac-Man hardware sprite rendering.

The lab has a verified board model, but visual sprite placement is a separate projection layer.

## Coordinate layers

### Logical board coordinates

Authority:

- src/board.txt
- src/projected_board.json

These files define board width, walls, dots, power dots, traversable cells, Pac-Man start, and ghost starts.

The board verifier proves movement-path legality in this coordinate system.

### C64 character rendering coordinates

Authority:

- src/generate_asm.py
- src/generated.s

The maze is rendered as 8x8 C64 character cells.

### C64 hardware sprite coordinates

Authority:

- src/generate_asm.py
- src/generated.s

Pac-Man is rendered as C64 hardware sprite 0.

A hardware sprite is 24x21 pixels. Its coordinate origin is not the center of the visible Pac-Man body.

The visible Pac-Man body is generated inside the sprite cell, so it has transparent margin and radial body geometry.

## Calibrated projection

The current visual projection from board cell to hardware sprite coordinate is:

    def cell_sprite_x(x: int, left: int) -> int:
        return 17 + (left + x) * 8

    def cell_sprite_y(y: int, top: int) -> int:
        return 44 + (top + y) * 8

This projection was calibrated by visual review so Pac-Man sits more evenly between hallway walls.

## Invariant

Do not treat board projection as proof of sprite centering.

Board projection answers:

> Is this cell/path legal?

Sprite projection answers:

> Does the visible hardware sprite sit correctly over that legal cell?

Both are required for the lab to look correct.

## Recalibration triggers

Recheck sprite projection if any of these change:

- Pac-Man sprite radius
- Pac-Man sprite center
- Pac-Man mouth geometry
- maze wall character art
- maze path width
- text-cell origin
- screen border/layout offsets
- hardware sprite mode or size
