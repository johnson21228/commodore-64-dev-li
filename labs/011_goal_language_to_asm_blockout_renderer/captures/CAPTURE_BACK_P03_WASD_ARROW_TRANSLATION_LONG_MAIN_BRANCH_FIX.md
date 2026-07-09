# Capture Back: P03 WASD Arrow Translation Long Main Branch Fix

The cursor-key translation patch made the input section large enough that a direct 6502 relative branch back to `main` went out of range.

This patch converts relative branches back to `main` into short skip branches followed by absolute `JMP main`, preserving behavior while avoiding branch-distance limits.
