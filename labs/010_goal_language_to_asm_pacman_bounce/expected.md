# Expected — Lab 010 Pac-Man Hardware Sprite Interpolation

Lab 010 Milestone C.4 renders the projected Pac-Man board and animates Pac-Man as C64 hardware sprite 0.

Expected runtime behavior:

- black border
- black background
- custom blue wall glyphs
- centered yellow dot glyphs
- centered yellow power-dot glyphs
- Pac-Man is hardware sprite 0, not a character cell
- Pac-Man starts at the `P` cell from `board.txt`
- Pac-Man moves pixel-by-pixel between board-cell centers
- Pac-Man target cells stay on traversable board cells only
- Pac-Man never targets `#` walls
- Pac-Man never targets `X` outside cells
- dots disappear as Pac-Man reaches cells
- if the generated path completes, the border turns red and the program stops visibly

Not expected in this milestone:

- ghost movement
- scoring
- full game win/loss outcomes beyond visible stop
- computer vision

Board authority:

- `src/board.txt`
- `src/projected_board.json`

Generated assembly:

- `src/generated.s`

Generated assembly is an artifact derived from the verified board contract.


## Milestone C.5 sprite size and mouth animation

- Pac-Man hardware sprite should be smaller and centered over the hallway cell.
- Pac-Man should no longer overwhelm the maze walls.
- Pac-Man should alternate open-mouth and closed-mouth frames while moving.
- Direction still comes from the next board path target.


## Milestone C.6 sprite animation fix

- Sprite animation should copy all 512 bytes for eight hardware sprite frames.
- Open-mouth frames D0-D3 and closed-mouth frames D4-D7 should both be available at runtime.
- Pac-Man should move faster: one raster frame per interpolated pixel.
- Mouth animation should toggle more visibly while moving.


## Milestone C.7 sprite tuning

- Pac-Man diameter should be smaller than C.6.
- Pac-Man should read as a compact centered sprite, not a large blob over the maze.
- Mouth animation should be slower and less frantic.
- Movement speed stays at one raster frame per interpolated pixel.


## Milestone C.8 pace tuning

- Pac-Man movement pace is cut approximately in half.
- Runtime now waits two raster frames per interpolated pixel.
- Board/path authority remains unchanged.


## Milestone C.9 mouth crunch tuning

- Pac-Man movement pace remains C.8 half-speed.
- Mouth animation crunch pace is increased.
- Mouth now toggles every 8 frame-pixel updates instead of every 16.
- Board/path authority remains unchanged.


## Milestone C.10 vertical sprite art

- North/south Pac-Man art should use dedicated vertical sprites.
- Vertical sprites should not be a literal rotation of horizontal sprites.
- Vertical Pac-Man should visually match horizontal Pac-Man diameter and weight.
- Movement pace and mouth crunch timing remain unchanged from C.9.


## Milestone C.11 equal-footprint sprite art

- Horizontal and vertical Pac-Man sprites should use the same drawn pixel footprint.
- All directions use the same approximate body box: x=6..17 and y=4..15.
- Vertical Pac-Man should no longer look taller, heavier, or distorted versus horizontal Pac-Man.
- Direction is conveyed by mouth cutout, not by changing body size.


## Milestone C.12 radial vertical mouth

- Pac-Man sprites should be generated from the same radial body geometry in all directions.
- North/south mouth should be a real vertical wedge cutout.
- Vertical Pac-Man should use the same center, radius, and visual weight as horizontal Pac-Man.
- Movement pace and mouth crunch timing remain unchanged.


## Milestone C.13 sprite origin tuning

- Pac-Man sprite should be lowered by one pixel.
- Pac-Man should sit more evenly between the hallway wall above and the hallway wall below.
- Board/path authority remains unchanged.


## Milestone C.14 sprite X origin tuning

- Pac-Man sprite should be shifted left by one pixel.
- Pac-Man should sit more evenly between the left and right hallway walls.
- C.13 Y origin tuning remains unchanged.
- Board/path authority remains unchanged.


## Milestone C.15 sprite X origin retuning

- Pac-Man sprite should be shifted left two additional pixels from C.14.
- Effective X origin is now three pixels left of the earlier hardware-sprite position.
- Pac-Man should sit closer to the center between left and right hallway walls.
- C.13 Y origin tuning remains unchanged.
- Board/path authority remains unchanged.
