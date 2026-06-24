# C64 Constraint Map

This file keeps C64 constraints visible during design.

## Machine constraints

- CPU family: 6510 / 6502-family programming model.
- Default BASIC start for many `.prg` examples: `$0801`.
- Common screen memory default: `$0400`.
- Color RAM default region: `$D800`.
- VIC-II, SID, CIA, and I/O behavior matter and may differ by PAL/NTSC timing.

## Design constraints

Before proposing a C64 feature, ask:

- Is this BASIC, assembly, C, or mixed?
- Does it need raster timing?
- Does it need sprites, bitmap mode, charset mode, or text mode?
- Does it need sound effects, music, or no SID work yet?
- Does it need keyboard, joystick, or both?
- What is the output artifact and validation path?

## Warning

Do not assume modern memory, floating point speed, fonts, file systems, threads, networking, Unicode, or dynamic allocation patterns unless the project intentionally provides them.
