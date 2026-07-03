# Capture Back — Pac-Man C64 Character Projection

## Captured decision

Lab 010 should continue to use a C64 character/tile-map rendering path for the Pac-Man board, but the visual projection must not treat each logical board cell as a crude ROM character.

The board-only render proved the authority chain:

`board.txt` / `projected_board.json` → `generate_asm.py` → `generated.s` → C64 runtime

However, the visual review showed that the first board render is too crude:

- walls render as thick full blue block cells
- hallways feel too narrow
- dots render as ROM punctuation and are not centered in hallways
- power dots render as ordinary ROM characters rather than centered pellets

## Rule

Board cells define game logic.

Custom C64 character glyphs define visual appearance.

These are related, but they are not the same thing.

`src/board.txt` remains the board authority for movement, traversability, dots, walls, and later Pac-Man behavior.

The C64 renderer should project those cells into custom glyphs suitable for the 8x8 character grid.

## Current visual issue

The current renderer maps:

- `#` to a full blue block-like character
- `.` to the ROM period character
- `o` to the ROM `O` character
- path/outside/start cells to blank

That is acceptable only as a first proof of the data path.

It is not the desired long-term C64 board projection.

## Desired Milestone B.1

Add a C64 character projection layer before adding Pac-Man movement.

Milestone B.1 should keep the board-only scope:

- no Pac-Man movement
- no ghost movement
- no scoring
- no win/loss outcomes
- no computer vision

But it should improve the board render by adding custom character glyphs.

## Dot projection rule

Dots are board data, but the dot visual must be projected.

A dot cell should render as a centered small pellet within its 8x8 character cell.

A power-dot cell should render as a centered larger pellet within its 8x8 character cell.

Do not use the ROM period character as the long-term pellet glyph because it is not visually centered.

## Wall projection rule

Walls are board data, but the wall visual must be projected.

A wall cell does not have to render as a full filled block.

The renderer may inspect neighboring board cells and choose custom thin-wall glyphs, such as:

- horizontal wall segment
- vertical wall segment
- corner wall segment
- junction / T segment if needed
- filled wall or outside block where appropriate

This keeps the logical board grid stable while making hallways visually wider and closer to a Pac-Man-style maze.

## Authority chain

The authority chain remains:

1. source board image
2. board projection LI
3. `src/board.txt`
4. `src/projected_board.json`
5. C64 character projection rules
6. generated C64 character data and screen map
7. generated assembly
8. C64 runtime behavior

Generated assembly remains an artifact.

The board authority remains `board.txt` plus `projected_board.json`.

## Implementation direction

The next refinement should be:

1. keep `board.txt` unchanged
2. add custom character data in generated assembly
3. point the C64 character memory register to the custom character set
4. map `.` to a centered pellet glyph
5. map `o` to a centered power-pellet glyph
6. map `#` to neighbor-aware thin-wall glyphs
7. verify generated assembly still derives from `board.txt`

## Workbench / LI principle

Language and image define intent.

Board data proves game logic.

C64 character projection defines visual fit.

Assembly is generated from verified contracts.

Runtime review checks whether the projection looks right.
