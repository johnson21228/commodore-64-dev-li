# Capture Back: C64 Hello World App

## Summary

Created a concrete first C64 Learning Lab app: `labs/001_hello_screen`.

The app is a small cc65 C program that clears the C64 screen, sets simple colors, prints `HELLO, WORLD!`, and waits for a key.

## Decision

Lab 001 is the first proof of the emulator-first learning loop:

```text
edit source -> build .prg -> run in VICE -> observe result -> capture evidence
```

## Added / updated

```text
labs/001_hello_screen/src/main.c
labs/001_hello_screen/README.md
labs/001_hello_screen/expected.md
docs/c64/hello_world_app.md
prompts/c64_run_hello_world_lab.md
cards/005_c64_hello_world_app_card.md
Makefile
tools/verify_c64_learning_lab.py
```

## Human review required

This CB does not claim emulator success. The next step is to build the `.prg` locally and observe it in VICE.
