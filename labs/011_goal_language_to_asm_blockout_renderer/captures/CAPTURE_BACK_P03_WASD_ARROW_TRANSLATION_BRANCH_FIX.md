# Capture Back: P03 WASD Arrow Translation Branch Fix

The first arrow-translation patch added cursor-key branches using direct BEQ labels. After the orientation handlers and movement handlers were inserted, the branch to `key_up` exceeded the 6502 relative branch range.

This patch replaces the cursor-key direct BEQs with near BNE guards plus absolute JMP trampolines. The runtime behavior is unchanged: cursor keys update XPOS/YPOS and redraw the selected orientation+cursor pose payload.
