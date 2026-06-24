# Commodore 64 Development Workbench LI

A Workbench for learning, designing, building, and preserving continuity around Commodore 64 software development.

This repo was created from the Workbench LI template and keeps the template governance intact. Its domain layer adds a C64 development spine: cross-development on a modern Mac, emulator-first validation, optional real-hardware handoff, and careful capture of toolchain decisions.

## C64 Learning Lab

The primary project direction is `C64 Learning Lab`: a sequence of small, runnable experiments that teach Commodore 64 machine concepts one at a time.

The Learning Lab loop is:

```text
C64 concept truth -> tiny runnable program -> emulator evidence -> verifier -> Capture Back
```

Start with:

```text
docs/c64/learning_lab_project_setup.md
docs/c64/lab_sequence.md
li/domain/c64_learning_lab_principles.md
li/domain/lab_artifact_contract.md
```

Verify the lab layer with:

```bash
make verify-learning-lab
```

## What this Workbench is for

Use this Workbench to develop small Commodore 64 programs, demos, games, experiments, and learning notes with durable AI-assisted continuity.

The initial posture is:

- write code on the modern machine;
- build reproducible `.prg` outputs;
- run first in a C64 emulator;
- document exact assumptions about memory, video, sound, input, and disk/tape output;
- only treat generated artifacts as evidence, not authority.

## First session

Start with:

```text
prompts/c64_interview_me_to_define_first_project.md
```

Then use one of:

```text
prompts/c64_create_first_hello_world.md
prompts/c64_design_sprite_or_charset_experiment.md
```

## C64 domain read-first files

```text
docs/c64/first_session_c64_hello_world.md
docs/c64/toolchain_options.md
source/c64/toolchain_source_map.md
li/domain/c64_development_principles.md
li/domain/cross_development_model.md
li/domain/emulator_first_hardware_later.md
li/domain/c64_constraints.md
li/domain/toolchain_source_authority.md
```

## Template governance still applies

Before changing this repo, read:

```text
LLM_READ_FIRST.md
HOW_LI_RULES.md
SPINE.md
MAP.md
li/workflow/workbench_build_loop.md
```

## Validation

```bash
make verify
```

This runs the template checks and the C64 Workbench domain check.

## Pack for ChatGPT / II handoff

```bash
make pack
```

The generated pack appears under `dist/` and excludes generated pack archives and local scratch material according to the template's Work Area Contract.
