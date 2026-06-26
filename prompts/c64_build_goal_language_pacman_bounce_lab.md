# Build / Continue C64 Lab 010: Goal-Language Pac-Man Bounce

Continue the authoritative Lab 010 at:

`labs/010_goal_language_to_asm_pacman_bounce/`

Preserve the goal-language-to-assembly chain:

`goal.lang -> program.lang -> generated_intent.json -> generated.s`

Required behavior:

- no `src/main.c`
- represent motion with signed `dx_vel` and `dy_vel`
- bounce by reflecting the hit axis of the vector
- animate the mouth open/closed
- derive open-mouth orientation from `direction_from_vector(dx_vel, dy_vel)`
- support `E`, `NE`, `N`, `NW`, `W`, `SW`, `S`, `SE`
- do not regress to left/right-only mouth selection
