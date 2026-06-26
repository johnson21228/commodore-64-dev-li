# Lab 010: Goal-Language to Assembly — Pac-Man Bounce

Lab 010 is the authoritative Pac-Man lab.

It keeps the goal-language-to-assembly path:

`goal.lang -> program.lang -> generated_intent.json -> generated.s`

The behavior contract is now vector-owned:

- motion is represented by signed `dx_vel` and `dy_vel`
- boundary collisions update the movement vector
- the mouth opens and closes as a crunching animation
- when open, the mouth faces `direction_from_vector(dx_vel, dy_vel)`
- supported open-mouth directions are `E`, `NE`, `N`, `NW`, `W`, `SW`, `S`, and `SE`
- left/right-only mouth selection is not sufficient
- no `src/main.c` is used
