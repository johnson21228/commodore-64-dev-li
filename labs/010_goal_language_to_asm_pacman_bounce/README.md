# Lab 010 — Pac-Man Buffered-Turn Hardware Sprite

This lab rebuilds a Pac-Man-style C64 runtime from a board-first LI pipeline.

The source board image is visual input, not runtime authority. The board is projected into reviewable data, verified, and then generated into C64 assembly.

## Current milestone

Milestone D.8: buffered-turn Pac-Man movement with W/A/S/D keyboard fallback.

The generated C64 program renders the Pac-Man board with custom characters and animates Pac-Man as hardware sprite 0.

Pac-Man movement is constrained by `src/board.txt`:

- `#` blocks movement
- `X` blocks movement
- `.`, `o`, space, `P`, and `G` are traversable

Pac-Man starts at the `P` cell and is initialized with a legal first target so he begins moving immediately.

## Current movement rule

Pac-Man uses Pac-Man-style continuous movement with buffered turn requests.

Input does not push Pac-Man one cell at a time.

Input records a requested direction.

At board-cell centers:

1. If the buffered requested direction is legal, Pac-Man turns.
2. If the buffered requested direction is blocked, Pac-Man continues current direction if legal.
3. If current direction is also blocked, Pac-Man stops at the cell center.

Pac-Man must not auto-select turns at hallway ends.

## Controls

Joystick port 2 is read from `$dc00` when VICE or hardware mapping is valid.

D.8 also adds W/A/S/D keyboard fallback into the same requested-direction buffer:

- W = up
- A = left
- S = down
- D = right

Use W/A/S/D for local VICE testing before relying on joystick mapping.

## Authority chain

1. `assets/source_board.png`
2. `BOARD_PROJECTION_LI.md`
3. `src/board.txt`
4. `src/projected_board.json`
5. `li/sprite_projection_contract.md`
6. `li/pacman_movement_contract.md`
7. `li/pacman_increment_ledger.md`
8. `src/generate_asm.py`
9. `src/generated.s`
10. C64 runtime review

`src/generated.s` is an artifact.

Board legality authority is `src/board.txt` plus `src/projected_board.json`.

Sprite visual registration authority is `li/sprite_projection_contract.md`.

Movement behavior authority is `li/pacman_movement_contract.md`.

Increment history authority is `li/pacman_increment_ledger.md`.

## Current generated runtime features

- C64 PRG load address `$0801`
- BASIC autostart line `10 SYS 2061`
- board rendered from verified board data
- custom C64 character set for walls/dots
- Pac-Man hardware sprite 0
- radial Pac-Man sprite art
- open/closed mouth animation
- pixel interpolation between board-cell centers
- generated legal-move masks from `board.txt`
- requested-direction buffer
- joystick input into requested-direction buffer
- W/A/S/D keyboard fallback into requested-direction buffer
- no generated random path tables
- no auto-turning

## Superseded experiment

D.6 auto-turning was an experiment and is superseded.

Auto-turning kept Pac-Man moving at hallway ends, but it was not canonical Pac-Man behavior.

The correct behavior is buffered player turn requests.

## Verify

From the repo root:

    python3 labs/010_goal_language_to_asm_pacman_bounce/src/verify_projected_board.py
    python3 tools/verify_c64_goal_language_to_asm_pacman_bounce_lab.py
    make verify

From the lab directory:

    make regenerate
    make build
    make run


## E.1 — Assembly efficiency gold

E.1 makes the generated board renderer compact.

The learning surface remains `goal.lang`, `program.lang`, LI contracts, generated intent, and runtime review. Under the hood, generated assembly should be efficient.

The board renderer now uses compact `board_render_row_*` character tables and a row/column loop.

This supersedes unrolled per-cell screen/color writes.

Board audit authority remains in `src/board.txt` and `src/projected_board.json`.
