# Lab 010 — Pac-Man Random Path Walker

This lab is being rebuilt around a board-first LI pipeline.

The source board image is visual input, not runtime authority. The board must first be projected into reviewable data, then verified, then generated into C64 assembly.

## Current milestone

Milestone C: Pac-Man random path walker.

The generated C64 program renders the board with custom characters and animates Pac-Man over legal board paths.

Pac-Man movement is constrained by `src/board.txt`:

- `#` blocks movement
- `X` blocks movement
- `.`, `o`, space, `P`, and `G` are traversable

Pac-Man starts at the `P` cell.

The generated path is produced from the verified board model and checked by the verifier before commit.

## Authority chain

1. `assets/source_board.png`
2. `BOARD_PROJECTION_LI.md`
3. `src/board.txt`
4. `src/projected_board.json`
5. generated legal Pac-Man path
6. `src/generated.s`
7. C64 runtime review

`src/generated.s` is an artifact. The board authority is `src/board.txt` plus `src/projected_board.json`.

## Verify

- `python3 src/verify_projected_board.py`
- `make regenerate`
- `python3 ../../tools/verify_c64_goal_language_to_asm_pacman_bounce_lab.py`


## Milestone C.1 — Pac-Man visual movement refinement

Pac-Man now uses directional custom character glyphs:

- east-facing
- west-facing
- north-facing
- south-facing

The glyph is larger, filling most of the hallway cell with a small inset.

The runtime chooses the Pac-Man glyph from the next path direction, so the mouth faces the direction of motion.

Movement is intentionally slowed for visual review.


## Milestone C.2 — Larger directional Pac-Man glyphs

Pac-Man now uses larger directional 8x8 custom character glyphs.

The glyphs are designed to fill nearly the full hallway cell while retaining a small inset.

The vertical glyphs are explicitly reviewed:

- north-facing Pac-Man uses a top mouth cutout
- south-facing Pac-Man uses a bottom mouth cutout

Movement remains board-constrained.


## Milestone C.3 — Vertical Pac-Man correction

The north/south Pac-Man custom characters were corrected.

The vertical glyphs now keep a round-ish full-cell body and use a top/bottom mouth notch, instead of tapering the whole body into a pentagon.
