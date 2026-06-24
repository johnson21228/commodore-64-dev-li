# Lab 003: Color Memory

## Status

Planned starter lab. The exact build command may require local cc65/VICE setup.

## Machine concept

This lab teaches how to write to C64 color RAM at $D800.

## Artifact

Expected build output:

```text
dist/color_memory.prg
```

## Build

From this lab folder:

```bash
make
```

## Run

Example VICE command, adjusted for local installation:

```bash
x64sc dist/color_memory.prg
```

## Expected observation

When run in the emulator, a character changes foreground color.

## Evidence

Capture the build command, launch command, and a short observation note or screenshot before claiming the lab complete.
