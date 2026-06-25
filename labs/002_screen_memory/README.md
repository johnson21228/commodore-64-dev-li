# Lab 002: Screen Memory

## Status

Runnable starter app.

## Purpose

This lab is the first direct-memory C64 example. It moves past console helpers and writes character codes directly into C64 screen RAM.

The lab proves this machine loop:

```text
C source -> cc65 .prg -> write bytes to $0400 -> observe characters on C64 screen
```

## Machine concept

The default C64 text screen uses 1000 character cells: 40 columns by 25 rows. In the normal startup memory map, screen RAM begins at hexadecimal address `$0400`.

This program treats `$0400` as an array:

```c
#define SCREEN ((volatile uint8_t*)0x0400)
```

Then it computes a row/column offset:

```text
offset = row * 40 + column
```

For example:

```text
row 10, col 5 -> 10 * 40 + 5 -> 405
```

## Artifact

Expected build output:

```text
dist/screen_memory.prg
```

## Build

From this lab folder:

```bash
make build
```

Or from the repo root:

```bash
make lab002
```

## Run

From this lab folder:

```bash
x64sc dist/screen_memory.prg
```

Or from the repo root, if `x64sc` is on your path:

```bash
make lab002-run
```

## Expected observation

When run in the emulator, the screen clears and shows:

```text
C64 LEARNING LAB
LAB 002 SCREEN MEMORY
WRITING TO $0400
TOP LEFT IS SCREEN[0]
ROW 10 COL 5 IS OFFSET 405
CLOSE EMULATOR TO END
```

The top-left character cell should contain a red `A`, proving that `SCREEN[0]` maps to the first visible screen cell.

## Evidence

Capture the build command, launch command, and one of:

- a screenshot of the emulator screen;
- a short observation note that the red `A` appeared in the top-left cell;
- a copied observation note in `work/runs/`.
