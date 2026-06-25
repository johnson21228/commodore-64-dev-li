# Card 005: C64 Hello World App

## Intent

Make the first Learning Lab program concrete and runnable.

## Change

Lab 001 now contains a Hello World C64 app that clears the screen, sets colors, prints fixed-position text, and waits for a key.

Root Makefile shortcuts were added:

```text
make lab001
make lab001-run
```

## Files

```text
labs/001_hello_screen/src/main.c
labs/001_hello_screen/README.md
labs/001_hello_screen/expected.md
docs/c64/hello_world_app.md
prompts/c64_run_hello_world_lab.md
```

## Verification

`make verify` checks that the Hello World lab source, docs, prompt, and root Makefile targets are present.

## Completion boundary

The app is structurally ready. The lab is complete only after a human builds and observes it in VICE or on real hardware.
