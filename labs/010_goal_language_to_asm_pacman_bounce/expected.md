# Expected — Lab 010 Board-Only Render

Lab 010 Milestone B renders the projected Pac-Man board as C64 screen output.

Expected runtime behavior:

- black border
- black background
- blue wall cells
- yellow dot cells
- yellow power-dot cells
- blank traversable path cells
- blank outside / non-playable cells
- infinite idle loop after rendering

Not expected in this milestone:

- Pac-Man movement
- ghost movement
- scoring
- dot eating
- win/loss outcomes
- image parsing / computer vision

Board authority:

- src/board.txt
- src/projected_board.json

Generated assembly:

- src/generated.s

Generated assembly is an artifact derived from the verified board contract.
