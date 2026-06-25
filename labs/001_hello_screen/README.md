# Lab 001: Hello Screen

## Status

Runnable starter app.

## Purpose

This is the first C64 Learning Lab application. It proves the basic loop:

```text
edit C on Mac -> build .prg with cc65 -> run in VICE -> observe C64 screen
```

## Machine concept

This lab introduces the C64 screen as the first visible proof surface. It uses cc65's C64 console helpers to clear the screen, set colors, place text, and wait for a key.

## Artifact

Expected build output:

```text
dist/hello_screen.prg
```

## Build

From this lab folder:

```bash
make build
```

Or from the repo root:

```bash
make lab001
```

## Run

From this lab folder:

```bash
x64sc dist/hello_screen.prg
```

Or from the repo root, if `x64sc` is on your path:

```bash
make lab001-run
```

## Expected observation

When run in the emulator, the C64 screen clears and shows:

```text
C64 LEARNING LAB
HELLO, WORLD!
LAB 001: HELLO SCREEN
BUILD: CC65 -> .PRG
RUN: VICE / X64SC
PRESS ANY KEY TO END
```

## Evidence

Capture the build command, launch command, and one of:

- a short terminal note that VICE launched the program;
- a screenshot of the emulator screen;
- a copied observation note in `work/runs/`.
