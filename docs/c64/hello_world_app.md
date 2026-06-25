# C64 Hello World App

The first runnable app in the C64 Learning Lab is `labs/001_hello_screen`.

It is intentionally small: one C file, one Makefile, one expected-result note, and one `.prg` artifact after build. In this Workbench, generated `.prg` artifacts are evidence, not source authority.

## Why this app matters

Hello World is not just a greeting. In this Workbench it proves the first complete C64 lab loop:

```text
source edit -> cc65 build -> .prg artifact -> VICE emulator run -> observed evidence -> Capture Back
```

## App behavior

The app clears the C64 screen, sets simple colors, places text at fixed coordinates, and waits for a key.

Expected visible text:

```text
C64 LEARNING LAB
HELLO, WORLD!
LAB 001: HELLO SCREEN
BUILD: CC65 -> .PRG
RUN: VICE / X64SC
PRESS ANY KEY TO END
```

## Build from repo root

```bash
make lab001
```

## Run from repo root

```bash
make lab001-run
```

`lab001-run` requires `x64sc` from VICE to be available on the shell path. If it is not, build the `.prg` and open it manually in VICE.

## Build from lab folder

```bash
cd labs/001_hello_screen
make build
x64sc dist/hello_screen.prg
```

## Completion rule

Do not claim the lab is complete until a human has observed the app running in VICE or on hardware and captured the observation.
