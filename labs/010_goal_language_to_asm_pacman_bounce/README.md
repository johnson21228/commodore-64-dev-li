# Lab 010: Goal-Language to Assembly — Pac-Man Bounce

This lab uses a tiny goal-language file to generate a C64-style Pac-Man bounce program.

The output is generated assembly, not C.

The current runtime is arcade-optimized for the mouth path:

- motion is represented by signed `dx` and `dy`
- boundary collisions update that vector
- `direction_index` caches the current movement direction
- `refresh_direction_index_01` runs only when a bounce changes `dx_vel` or `dy_vel`
- the mouth opens and closes as a crunching animation
- `mouth_dirty` marks whether the sprite pointer may need to change
- `apply_mouth_pointer_if_dirty_01` uses `mouth_pointer_table_01,x`
- `$07f8` is written only at the single cached pointer update site
- supported open-mouth directions are `E`, `NE`, `N`, `NW`, `W`, `SW`, `S`, and `SE`
- left/right-only mouth selection is not enough

The learning goal is to show that a higher-level intent sentence can be lowered into speed-first assembly evidence while preserving a real gameplay invariant.
