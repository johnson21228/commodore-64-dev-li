# Card 007: C64 Color Memory App

## Summary

Promote Lab 003 from skeleton to runnable app.

## Decision

Lab 003 teaches that C64 character display and character foreground color are controlled by paired offsets in different memory regions:

```text
SCREEN RAM: $0400
COLOR  RAM: $D800
```

## Files

- `labs/003_color_memory/src/main.c`
- `labs/003_color_memory/README.md`
- `labs/003_color_memory/expected.md`
- `docs/c64/color_memory_app.md`
- `prompts/c64_run_color_memory_lab.md`
- `captures/CAPTURE_BACK_C64_COLOR_MEMORY_APP.md`

## Verification

`tools/verify_c64_learning_lab.py` checks the Lab 003 app files, required explanatory tokens, and root Makefile shortcuts.

## Follow-up

After emulator evidence is captured, the next lab should introduce PETSCII layout or keyboard input, depending on whether the learning path prioritizes visual UI or interaction.
