# Lab 002: Screen Memory

## Status

Planned starter lab. The exact build command may require local cc65/VICE setup.

## Machine concept

This lab teaches how to write directly to C64 screen RAM at $0400.

## Artifact

Expected build output:

```text
dist/screen_memory.prg
```

## Build

From this lab folder:

```bash
make
```

## Run

Example VICE command, adjusted for local installation:

```bash
x64sc dist/screen_memory.prg
```

## Expected observation

When run in the emulator, a character appears at a chosen screen position.

## Evidence

Capture the build command, launch command, and a short observation note or screenshot before claiming the lab complete.
