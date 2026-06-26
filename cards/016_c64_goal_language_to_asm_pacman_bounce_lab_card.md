# Card 016: C64 Goal-Language Pac-Man Bounce Lab

## Purpose

Preserve Lab 010 as the goal-language Pac-Man bounce lab while adding the vector-facing mouth invariant and an arcade-optimized runtime path.

## Rule

Pac-Man mouth orientation is derived from the signed `dx/dy` movement vector. It is not selected from left/right state alone.

## Runtime optimization

The generated assembly stores a cached `direction_index`, marks pointer work with `mouth_dirty`, and selects the sprite frame through `mouth_pointer_table_01,x`. Clean frames avoid writing `$07f8`.

## Evidence

- `labs/010_goal_language_to_asm_pacman_bounce/src/goal.lang`
- `labs/010_goal_language_to_asm_pacman_bounce/src/program.lang`
- `labs/010_goal_language_to_asm_pacman_bounce/src/generate_asm.py`
- `labs/010_goal_language_to_asm_pacman_bounce/src/generated.s`
- `labs/010_goal_language_to_asm_pacman_bounce/src/generated_intent.json`
- `tools/verify_c64_goal_language_to_asm_pacman_bounce_lab.py`
