# C64 Screen Memory App

## Purpose

This document defines the second runnable C64 Learning Lab application: **Lab 002: Screen Memory**.

The lab teaches the first direct hardware-facing idea in the Workbench:

```text
visible C64 screen cell <- byte written into screen RAM at $0400
```

## What the app demonstrates

The app writes directly to C64 memory addresses instead of using high-level console output helpers.

It introduces:

- `$0400` as the default C64 screen RAM base address;
- the 40-column by 25-row text grid;
- row/column offset calculation;
- C64 screen codes;
- `volatile` pointers for memory-mapped output;
- emulator observation as evidence.

## Why this follows Hello World

Lab 001 proves that the toolchain can build and run a `.prg`.

Lab 002 proves that generated code can touch the C64 machine model directly:

```text
source code -> memory address -> visible machine behavior
```

That is the Learning Lab pattern.

## Expected visible proof

The app should show title text and a red `A` in the top-left character cell.

The red `A` matters because it is the smallest possible proof:

```text
SCREEN[0] = screen_code('A')
```

If the top-left cell changes, the learner has observed the mapping between `$0400` and the visible display.

## Build and run

From the Workbench root:

```bash
make lab002
make lab002-run
```

Expected artifact:

```text
labs/002_screen_memory/dist/screen_memory.prg
```

## Boundary

This lab is still emulator-first. Do not claim real C64 hardware behavior unless it is run on real hardware and captured separately.
