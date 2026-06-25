# Card 006: C64 Screen Memory App

## Status

Accepted.

## Intent

Promote Lab 002 from a planned skeleton into a runnable C64 Learning Lab app that demonstrates direct writes to screen RAM at `$0400`.

## Adds

- `docs/c64/screen_memory_app.md`
- `prompts/c64_run_screen_memory_lab.md`
- `captures/CAPTURE_BACK_C64_SCREEN_MEMORY_APP.md`
- root `make lab002` and `make lab002-run` shortcuts
- runnable `labs/002_screen_memory/src/main.c`

## Learning claim

The lab teaches that the default C64 text screen is a memory-mapped 40x25 character grid beginning at `$0400`.

## Evidence expectation

A valid emulator run shows Lab 002 text and a red `A` in the top-left cell, proving that `SCREEN[0]` affects the first visible character position.

## Verification

`tools/verify_c64_learning_lab.py` must require the Lab 002 app doc, prompt, card, capture, source tokens, and root Makefile shortcuts.
