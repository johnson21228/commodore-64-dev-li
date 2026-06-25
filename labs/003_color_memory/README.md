# Lab 003: Color Memory

## Purpose

This lab shows that C64 screen characters and their foreground colors live in paired but separate memory regions.

```text
SCREEN RAM: $0400
COLOR  RAM: $D800
```

`SCREEN[0]` controls the top-left character. `COLOR[0]` controls that character's foreground color.

## Build

From the repo root:

```bash
make lab003
```

Or from this lab folder:

```bash
make build
```

## Run

From the repo root:

```bash
make lab003-run
```

This expects VICE's `x64sc` command to be installed and available on `PATH`.

## Expected artifact

```text
dist/color_memory.prg
```

## Expected observation

The emulator should show the Lab 003 explanatory text and colored `A`, `B`, and `C` characters. The lesson is that writing to `$0400` changes visible characters, while writing to `$D800` changes the foreground colors for the same offsets.
