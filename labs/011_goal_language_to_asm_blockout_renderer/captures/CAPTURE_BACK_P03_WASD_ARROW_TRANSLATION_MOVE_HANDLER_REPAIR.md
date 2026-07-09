# Capture Back: P03 WASD Arrow Translation Move Handler Repair

The previous broad branch-range repair left the Python `move_handler` block mis-indented. This patch replaces the whole movement-handler generator with a known-good form.

Movement remains bounded to the current 3x3 pit cursor grid and uses absolute `JMP main` returns to avoid 6502 branch-distance limits.
