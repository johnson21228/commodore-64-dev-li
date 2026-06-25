# Capture Back: C64 Color Memory App

## What changed

The Commodore 64 Learning Lab now has a concrete Lab 003 app: `Color Memory`.

## Why

Lab 002 proved that writing to `$0400` changes visible screen characters. Lab 003 adds the companion machine concept: C64 color RAM starts at $D800, and writing to `$D800` changes the foreground color for the same screen-cell offset.

## Learning claim

```text
SCREEN[0] at $0400 controls the top-left character.
COLOR[0] at $D800 controls the top-left character's foreground color.
```

This creates the first paired C64 memory model in the lab.

## App behavior

The app displays explanatory text and writes colored `A`, `B`, and `C` characters using direct writes to screen RAM and color RAM.

Expected text includes:

```text
C64 LEARNING LAB
LAB 003 COLOR MEMORY
SCREEN RAM: $0400
COLOR  RAM: $D800
COLOR[0] COLORS SCREEN[0]
A B C USE DIFFERENT COLORS
CLOSE EMULATOR TO END
```

## New files

- `docs/c64/color_memory_app.md`
- `prompts/c64_run_color_memory_lab.md`
- `cards/007_c64_color_memory_app_card.md`
- `captures/CAPTURE_BACK_C64_COLOR_MEMORY_APP.md`

## Updated files

- `labs/003_color_memory/src/main.c`
- `labs/003_color_memory/README.md`
- `labs/003_color_memory/expected.md`
- `Makefile`
- `MAP.md`
- `SPINE.md`
- `README.md`
- `tools/verify_c64_learning_lab.py`
- `tools/verify_c64_workbench.py`

## Commands

```bash
cd /Users/stevejohnson/Developer/commodore-64-dev-li

make verify
make lab003
make lab003-run
```

## Boundary

This Capture Back does not claim that the app has been built or observed on the user's Mac. It only adds the source, documentation, prompts, and verification structure. Build/emulator evidence should be captured after `cl65` and VICE are available locally.
