# Capture Back: C64 Goal-Language Pac-Man Bounce Lab

Lab 010 is the authoritative Pac-Man bounce lab.

Update captured:

- preserve `labs/010_goal_language_to_asm_pacman_bounce/`
- keep motion as signed `dx/dy`
- derive open-mouth orientation from the movement vector
- support cardinal and diagonal mouth directions
- reject left/right-only mouth direction as insufficient
- optimize the generated assembly runtime with a cached `direction_index`
- update the mouth sprite pointer only through the `mouth_dirty` / `mouth_pointer_table_01,x` path

Verification:

```bash
python3 tools/verify_c64_goal_language_to_asm_pacman_bounce_lab.py
make verify
make pack
```
