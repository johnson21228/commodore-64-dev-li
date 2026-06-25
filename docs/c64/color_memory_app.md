# C64 Learning Lab 003: Color Memory

## Purpose

Lab 003 turns the Lab 002 screen-memory idea into the next machine concept: C64 color RAM.

Lab 002 showed that C64 screen RAM starts at `$0400` and that `SCREEN[0]` maps to the top-left visible character cell.

Lab 003 adds the paired color-memory fact:

```text
C64 color RAM starts at $D800.
COLOR[0] controls the foreground color of SCREEN[0].
```

## App behavior

The app writes visible characters into screen RAM and writes color values into matching color RAM cells.

Expected screen text:

```text
C64 LEARNING LAB
LAB 003 COLOR MEMORY
SCREEN RAM: $0400
COLOR  RAM: $D800
COLOR[0] COLORS SCREEN[0]
A B C USE DIFFERENT COLORS
CLOSE EMULATOR TO END
```

The top-left demonstration writes `A`, `B`, and `C` directly into screen RAM and assigns different color values to each matching color cell.

## Build

```bash
cd /Users/stevejohnson/Developer/commodore-64-dev-li
make lab003
```

The generated program should be:

```text
labs/003_color_memory/dist/color_memory.prg
```

## Run

```bash
cd /Users/stevejohnson/Developer/commodore-64-dev-li
make lab003-run
```

If `x64sc` is not installed, open the generated `.prg` manually in a C64 emulator.

## Learning claim

Lab 003 is complete when emulator evidence shows that screen characters and their foreground colors are controlled by different memory regions.

The key observation is:

```text
Writing to $0400 changes what character is displayed.
Writing to $D800 changes that character's foreground color.
```

## Boundary

This lab does not yet teach full VIC-II color control, background colors, raster timing, sprites, or character-set redefinition. It only introduces the paired screen/color memory model.
