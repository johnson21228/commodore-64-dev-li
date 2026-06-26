# Card 016: C64 Goal-Language Pac-Man Bounce Lab

## Purpose

Lab 010 demonstrates a goal-language-to-assembly Pac-Man bounce app.

## Updated invariant

The Pac-Man mouth faces the signed `dx_vel` / `dy_vel` movement vector, not just left or right.

## Evidence

- `labs/010_goal_language_to_asm_pacman_bounce/src/goal.lang`
- `labs/010_goal_language_to_asm_pacman_bounce/src/program.lang`
- `labs/010_goal_language_to_asm_pacman_bounce/src/generate_asm.py`
- `labs/010_goal_language_to_asm_pacman_bounce/src/generated_intent.json`
- `labs/010_goal_language_to_asm_pacman_bounce/src/generated.s`
- `tools/verify_c64_goal_language_to_asm_pacman_bounce_lab.py`
