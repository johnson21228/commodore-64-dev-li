# Expected Result

Lab 010 generates assembly-only C64 evidence for a yellow Pac-Man style sprite.

Expected behavior:

- generated assembly is the app; no `src/main.c`
- sprite moves by signed `dx_vel` and `dy_vel`
- sprite bounces by reflecting the hit axis of the movement vector
- mouth toggles open/closed every eight frames
- open mouth faces the current vector direction
- cardinal directions are present: `E`, `N`, `W`, `S`
- diagonal directions are present: `NE`, `NW`, `SW`, `SE`
- the verifier rejects a duplicate standalone Pac-mouth Lab 010
