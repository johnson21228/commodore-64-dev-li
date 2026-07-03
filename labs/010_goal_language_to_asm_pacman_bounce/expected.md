# Expected — Lab 010 Pac-Man Buffered-Turn Hardware Sprite

## Current expected behavior

Lab 010 currently targets D.8: Pac-Man-style continuous movement with buffered requested turns and W/A/S/D keyboard fallback.

Expected runtime behavior:

- black border
- black background
- custom blue wall glyphs
- centered yellow dot glyphs
- centered yellow power-dot glyphs
- Pac-Man is hardware sprite 0, not a character cell
- Pac-Man starts at the `P` cell from `board.txt`
- Pac-Man has an immediate legal first target after startup
- Pac-Man moves pixel-by-pixel between board-cell centers
- Pac-Man target cells stay on traversable board cells only
- Pac-Man never targets `#` walls
- Pac-Man never targets `X` outside cells
- dots disappear as Pac-Man reaches cells
- mouth animation alternates open/closed frames while moving
- direction sprite follows current movement direction
- joystick port 2 input can update requested direction when mapped
- W/A/S/D keyboard fallback updates the same requested-direction buffer
- requested direction is applied only when legal at a board-cell center
- blocked requested turns are ignored
- Pac-Man continues current direction if legal
- Pac-Man stops at a cell center if current direction is blocked and no legal buffered turn exists
- Pac-Man does not auto-select turns

## Controls

Use W/A/S/D for the first playable VICE test:

- W = up
- A = left
- S = down
- D = right

Joystick port 2 remains supported through `$dc00`, but VICE joystick mapping may require configuration.

## Not expected yet

- ghost movement
- scoring
- full game win/loss outcomes
- fruit
- frightened mode
- power-pellet behavior
- collision rules
- complete Pac-Man timing model
- computer vision

## Authority

Board authority:

- `src/board.txt`
- `src/projected_board.json`

Sprite projection authority:

- `li/sprite_projection_contract.md`

Movement authority:

- `li/pacman_movement_contract.md`

Increment history authority:

- `li/pacman_increment_ledger.md`

Generated assembly:

- `src/generated.s`

Generated assembly is an artifact derived from the verified board and movement contracts.

## Increment expectations

### C.4 — Hardware sprite interpolation

Pac-Man is rendered as hardware sprite 0 and moves between board-cell centers.

### C.5 — Smaller animated sprite

Pac-Man uses open/closed mouth sprite frames for all four directions.

### C.6 — Sprite copy and speed fix

All 512 bytes for eight sprite frames are copied.

### C.7 — Smaller diameter and slower mouth

Pac-Man is visually smaller and centered in the hallway.

### C.8 — Half-speed movement

Pac-Man waits two raster frames per interpolated pixel.

### C.9 — Faster mouth crunch

Mouth animation toggles every 8 frame-pixel updates.

### C.10 — Dedicated vertical sprite art

North/south sprite art was explored.

### C.11 — Equal-footprint sprite art

All directions share a common visual footprint.

### C.12 — Radial sprite geometry

All directions are generated from one radial sprite geometry.

### C.13 — Y-origin tuning

Pac-Man sprite is lowered by one pixel.

### C.14 — X-origin tuning

Pac-Man sprite is shifted left by one pixel.

### C.15 — X-origin retuning

Pac-Man sprite is shifted left two additional pixels and sprite projection is captured as LI.

### D.1 — Joystick input experiment

Joystick port 2 was introduced as an input source.

### D.2 — BASIC autostart header

PRG includes BASIC `10 SYS 2061`.

### D.3 — PRG load address

PRG begins with two-byte load address `$0801`.

### D.4 — Continuous momentum

Pac-Man keeps current direction while legal.

### D.5 — Starting momentum

Pac-Man starts with an immediate legal first target.

### D.6 — Auto-turn experiment, superseded

Auto-turning is superseded and must not be regenerated.

### D.7 — Buffered requested turns

Input updates a requested-direction buffer. Requested turns are applied only when legal.

### D.8 — W/A/S/D keyboard fallback

W/A/S/D updates the same requested-direction buffer as joystick input.


## E.1 expected assembly efficiency

- Generated assembly should use a table-driven board renderer.
- Generated assembly should not include unrolled `; board[x,y]` render writes.
- Generated assembly should not embed audit-only `board_row_*` data.
- Board render characters should come from compact `board_render_row_*` tables.
- Runtime visual output should remain the same.
- Learning remains centered on the language and LI surface.
