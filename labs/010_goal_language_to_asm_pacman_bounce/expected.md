# Expected — Lab 010 Pac-Man Random Path Walker

Lab 010 Milestone C renders the projected Pac-Man board and animates Pac-Man over legal path cells.

Expected runtime behavior:

- black border
- black background
- custom blue wall glyphs
- centered yellow dot glyphs
- centered yellow power-dot glyphs
- yellow Pac-Man glyph
- Pac-Man starts at the `P` cell from `board.txt`
- Pac-Man moves from board cell to board cell
- Pac-Man stays on traversable cells only
- Pac-Man never enters `#` walls
- Pac-Man never enters `X` outside cells
- dots disappear when Pac-Man leaves a cell
- if the generated path completes, the border turns red and the program stops visibly

Not expected in this milestone:

- ghost movement
- scoring
- win/loss game outcomes beyond visible stop
- computer vision

Board authority:

- `src/board.txt`
- `src/projected_board.json`

Generated assembly:

- `src/generated.s`

Generated assembly is an artifact derived from the verified board contract.


## Milestone C.1 visual movement refinement

- Pac-Man movement should be slower and easier to visually review.
- Pac-Man should fill most of the hallway cell with only a small inset.
- Pac-Man mouth should face the direction of motion.
- Movement remains constrained to verified traversable board cells.


## Milestone C.2 Pac-Man glyph refinement

- Pac-Man should be larger within the 8x8 hallway cell.
- Pac-Man should keep only a small visual inset from the cell edge.
- East and west glyphs should have clear side-facing mouth cutouts.
- North and south glyphs should have clear top/bottom mouth cutouts.
- Movement remains constrained to verified traversable board cells.


## Milestone C.3 vertical Pac-Man correction

- North and south Pac-Man glyphs should no longer look like pentagons.
- Vertical Pac-Man should keep a round-ish full-cell body.
- The mouth should be a top or bottom notch, not a tapered body.
