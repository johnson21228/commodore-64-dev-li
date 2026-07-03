# Capture Back — Pac-Man Sprite Projection Contract

## Captured rule

Lab 010 has two coordinate systems that must not be conflated:

1. Logical board coordinates
   - Source authority: src/board.txt
   - Projected authority: src/projected_board.json
   - Meaning: maze cells, walls, dots, traversable cells, Pac-Man start, ghost starts

2. Visual sprite registration
   - Source authority: src/generate_asm.py
   - Runtime artifact: src/generated.s
   - Meaning: how a logical board cell maps to C64 hardware sprite pixel coordinates

The board projection can prove that Pac-Man is in a legal maze cell.

It does not, by itself, prove that the visible 24x21 hardware sprite is centered between the hallway walls.

## Why this matters

C64 text cells are 8x8 pixels.

C64 hardware sprites are 24x21 pixels.

Pac-Man's drawn body does not fill the entire 24x21 sprite cell. The visible Pac-Man body has its own center, radius, mouth wedge, and empty transparent margin inside the sprite.

Therefore a generated hardware sprite needs an explicit visual-registration contract.

## Current calibrated projection

As of the C.15 visual tuning pass, Pac-Man's hardware sprite placement is calibrated as:

    def cell_sprite_x(x: int, left: int) -> int:
        return 17 + (left + x) * 8

    def cell_sprite_y(y: int, top: int) -> int:
        return 44 + (top + y) * 8

This means:

- X origin is shifted left from the first hardware-sprite placement.
- Y origin is shifted down from the first hardware-sprite placement.
- The tuning is empirical, based on visual centering between hallway walls.
- The board/path authority is unchanged.

## Future rule

Future Lab 010 changes must preserve the distinction:

- Board legality is verified from board.txt / projected_board.json.
- Sprite visual centering is verified by the sprite projection contract.
- Do not claim source-board projection alone proves sprite alignment.
- If sprite art changes size, radius, center, or mouth geometry, revisit sprite visual registration.
- If wall/path rendering changes, revisit sprite visual registration.
