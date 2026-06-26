# Capture Back: C64 Goal-Language Pac-Man Bounce Lab

Cleanup captured:

- keep `labs/010_goal_language_to_asm_pacman_bounce/` as authoritative Lab 010
- remove duplicate `labs/010_pac_mouth_motion/`
- fold vector-facing mouth behavior into the goal-language Pac-Man bounce lab
- use signed `dx_vel` / `dy_vel` as the movement truth
- choose open-mouth frames from `direction_from_vector(dx_vel, dy_vel)`
- support `E`, `NE`, `N`, `NW`, `W`, `SW`, `S`, and `SE`
- restore `make verify` coverage for Lab 010 and Lab 011

Verification:

```bash
python3 tools/verify_c64_goal_language_to_asm_pacman_bounce_lab.py
python3 tools/verify_c64_goal_language_to_asm_net_proxy_lab.py
make verify
make pack
```
