# Prompt: Run C64 Learning Lab 003 Color Memory

Use this prompt when continuing the Commodore 64 Learning Lab.

## Goal

Build and run Lab 003, then capture what was observed.

## Context

Lab 003 teaches color RAM. Screen RAM starts at `$0400`; color RAM starts at `$D800`. A screen cell's character code and foreground color are controlled by paired offsets in separate memory regions.

## Commands

```bash
cd /Users/stevejohnson/Developer/commodore-64-dev-li

make verify
make lab003
make lab003-run
```

If `cl65` is missing, install cc65 before building. If `x64sc` is missing, install VICE or open the generated `.prg` manually.

## Expected artifact

```text
labs/003_color_memory/dist/color_memory.prg
```

## Expected observation

The C64 emulator should show the Lab 003 explanatory text and colored `A`, `B`, and `C` characters whose screen cells are written through `$0400` and whose foreground colors are written through `$D800`.

## Capture Back questions

1. Did `make lab003` build the `.prg`?
2. Did the emulator launch?
3. Were the colored characters visible?
4. What does the observation teach about screen RAM versus color RAM?
5. What should Lab 004 teach next?
