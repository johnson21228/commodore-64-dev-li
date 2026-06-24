# LLM Read First: Commodore 64 Development Workbench

You are entering a Workbench LI repo. Do not invent repo state. Read the repo files before proposing changes.

## First files to read

```text
MAP.md
SPINE.md
HOW_LI_RULES.md
li/workflow/workbench_build_loop.md
li/source/source_truth.md
li/source/authority_levels.md
```

For C64-specific work, then read:

```text
li/domain/c64_development_principles.md
li/domain/cross_development_model.md
li/domain/emulator_first_hardware_later.md
li/domain/c64_constraints.md
li/domain/toolchain_source_authority.md
source/c64/toolchain_source_map.md
```

## C64 work posture

Assume modern cross-development unless the human says otherwise. Prefer reproducible build commands, emulator validation, small experiments, and explicit capture of outcomes.

Do not claim a `.prg`, `.d64`, emulator run, or real-hardware test succeeded unless evidence is present in the repo or the human pasted the result.

## Capture Back posture

Capture Back should preserve durable learning, not every scratch thought. For C64, good Capture Back candidates include:

- confirmed toolchain setup;
- successful emulator run commands;
- memory-map decisions;
- sprite/charset/audio constraints;
- debugger findings;
- hardware transfer notes;
- failed assumptions that should not be repeated.

## Safety of generated artifacts

Generated code, images, binaries, and build scripts are evidence only until reviewed, built, and validated by the human.
