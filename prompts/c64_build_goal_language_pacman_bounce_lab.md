# Build / Continue C64 Lab 010: Goal-Language Pac-Man Bounce

Continue the authoritative Lab 010 at:

`labs/010_goal_language_to_asm_pacman_bounce/`

Preserve the goal-language-to-assembly flow.

Required behavior:

- represent motion with signed `dx/dy`
- bounce by changing the vector at boundaries
- animate the mouth open/closed
- derive open-mouth orientation from the movement vector
- support `E`, `NE`, `N`, `NW`, `W`, `SW`, `S`, `SE`
- do not regress to left/right-only mouth selection

Required optimization:

- cache direction in `direction_index`
- recompute direction only after bounce velocity changes
- gate sprite pointer writes with `mouth_dirty`
- select frame pointers with `mouth_pointer_table_01,x`
- keep generated output assembly-only; no `main.c`
