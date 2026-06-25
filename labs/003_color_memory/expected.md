# Expected: Lab 003 Color Memory

After building and running `dist/color_memory.prg`, the emulator should show:

```text
C64 LEARNING LAB
LAB 003 COLOR MEMORY
SCREEN RAM: $0400
COLOR  RAM: $D800
COLOR[0] COLORS SCREEN[0]
A B C USE DIFFERENT COLORS
CLOSE EMULATOR TO END
```

Direct memory evidence:

```text
SCREEN[0] at $0400 contains the character code for A.
COLOR[0] at $D800 contains the foreground color for that A.
SCREEN[2] and COLOR[2] form another paired character/color example.
SCREEN[4] and COLOR[4] form another paired character/color example.
```

Success means the lab demonstrates that C64 screen contents and character colors are separate memory-mapped concerns.
