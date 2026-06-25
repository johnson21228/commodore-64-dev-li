# Capture Back: C64 Screen Memory App

## Date

2026-06-25

## Summary

Added the next concrete C64 Learning Lab code example: **Lab 002: Screen Memory**.

This turns the screen-memory lab from a starter skeleton into a runnable `.prg` application.

## Decision

Lab 002 should teach direct memory-mapped screen output before moving to richer visual or input labs.

The lab uses this core machine claim:

```text
C64 screen RAM starts at $0400 in the default text screen configuration.
SCREEN[0] maps to the top-left visible character cell.
```

## Files added or updated

- `labs/002_screen_memory/src/main.c`
- `labs/002_screen_memory/README.md`
- `labs/002_screen_memory/expected.md`
- `docs/c64/screen_memory_app.md`
- `prompts/c64_run_screen_memory_lab.md`
- `cards/006_c64_screen_memory_app_card.md`
- `tools/verify_c64_learning_lab.py`
- `Makefile`
- `MAP.md`
- `SPINE.md`
- `README.md`

## Runtime behavior

The app writes directly to `$0400` and displays:

```text
C64 LEARNING LAB
LAB 002 SCREEN MEMORY
WRITING TO $0400
TOP LEFT IS SCREEN[0]
ROW 10 COL 5 IS OFFSET 405
CLOSE EMULATOR TO END
```

It also writes a red `A` to the top-left cell by assigning `SCREEN[0]`.

## Verification posture

The Workbench verifier checks that Lab 002 is present and documented. It does not claim emulator success by itself.

Actual completion of the lab still requires local build and emulator evidence:

```bash
make lab002
make lab002-run
```

## Boundary

This remains emulator-first. Do not claim real hardware success unless separately tested on real C64 hardware.
