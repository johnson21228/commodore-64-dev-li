# C64 Lab 010: Goal-Language Pac-Man Bounce

Lab 010 keeps the goal-language-to-assembly path, but strengthens the Pac-Man behavior contract and the generated assembly runtime.

The authoritative lab is:

`labs/010_goal_language_to_asm_pacman_bounce/`

The motion truth is the signed movement vector:

- `dx`
- `dy`

The mouth animation is not merely left/right. The open-mouth frame must be chosen from the movement vector so the mouth can face:

- `E`
- `NE`
- `N`
- `NW`
- `W`
- `SW`
- `S`
- `SE`

The optimized assembly path is arcade-style:

- `direction_index` stores the current compass direction
- `refresh_direction_index_01` runs only after a bounce changes `dx_vel` or `dy_vel`
- `mouth_dirty` tracks whether the sprite pointer might need a new value
- `apply_mouth_pointer_if_dirty_01` exits immediately on clean frames
- `mouth_pointer_table_01,x` maps closed/open-vector frame indexes to VIC sprite pointers
- there is one generated `sta SPRITE_POINTER_0` write site

This keeps Lab 010 as the real Pac-Man bounce lab and avoids both the old left/right-only shortcut and an every-frame mouth branch chain.
