# Prompt: Run C64 Screen Memory Lab

Use this prompt when continuing the C64 Learning Lab from Lab 002.

## Goal

Help me build and run `labs/002_screen_memory`, then capture the emulator evidence.

## Instructions

1. Read `LLM_READ_FIRST.md`, `SPINE.md`, and `MAP.md`.
2. Read `docs/c64/screen_memory_app.md`.
3. Inspect `labs/002_screen_memory/README.md`, `expected.md`, `Makefile`, and `src/main.c`.
4. Build with:

```bash
cd /Users/stevejohnson/Developer/commodore-64-dev-li
make lab002
```

5. Run with:

```bash
make lab002-run
```

6. If `cl65` or `x64sc` is missing, stop at the missing dependency and report the next installation step. Do not claim a run occurred.
7. If the emulator launches, capture the observation that a red `A` appears in the top-left character cell and the Lab 002 text appears on screen.
8. Propose a Capture Back only after the evidence is known.

## Evidence to capture

- build command and result;
- generated `.prg` path;
- emulator launch command;
- visual observation or screenshot;
- any dependency failure.
