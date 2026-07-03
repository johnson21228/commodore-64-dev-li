# Lab 010 — Pac-Man Board-Only Render

This lab is being rebuilt around a board-first LI pipeline.

The source board image is visual input, not runtime authority. The board must first be projected into reviewable data, then verified, then generated into C64 assembly.

Current milestone: Milestone B, board-only C64 render.

The generated C64 program renders walls, dots, power dots, empty paths, and outside cells.

It does not yet implement Pac-Man movement, ghosts, scoring, or game outcomes.

Authority chain:

1. assets/source_board.png
2. BOARD_PROJECTION_LI.md
3. src/board.txt
4. src/projected_board.json
5. src/generated.s
6. C64 runtime review

src/generated.s is an artifact. The board authority is src/board.txt plus src/projected_board.json.

Verify:

- python3 src/verify_projected_board.py
- make regenerate
- python3 ../../tools/verify_c64_goal_language_to_asm_pacman_bounce_lab.py
