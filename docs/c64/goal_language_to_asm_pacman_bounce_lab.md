# C64 Lab 010: Goal-Language Pac-Man Bounce

Lab 010 is the authoritative Pac-Man lab:

`labs/010_goal_language_to_asm_pacman_bounce/`

The lab keeps the original goal-language-to-assembly custody chain, but updates Pac-Man behavior so mouth orientation observes the full movement vector.

Required invariant:

- `dx_vel` and `dy_vel` are the movement truth
- boundary bounces reflect the hit axis of the vector
- mouth animation toggles open/closed
- open mouth orientation is selected by `direction_from_vector(dx_vel, dy_vel)`
- supported directions are `E`, `NE`, `N`, `NW`, `W`, `SW`, `S`, and `SE`
- a left/right-only mouth selector is stale and insufficient
- no `src/main.c` participates in Lab 010

This merges the experimental Pac-mouth motion work into the existing Pac-Man bounce lab instead of keeping a second Lab 010.
