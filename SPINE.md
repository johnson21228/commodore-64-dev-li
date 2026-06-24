# Commodore 64 Development Workbench LI Spine

## Purpose

This repository exists to preserve continuity for Commodore 64 development: learning, design, build decisions, toolchain choices, emulator validation, hardware notes, and future handoff.

## Governing idea

Modern AI-assisted reasoning can help with old-machine development only when the repo keeps strict custody of source context, hardware constraints, toolchain facts, generated evidence, and human decisions.

## Development posture

The default posture is cross-development:

1. edit and build on the modern machine;
2. produce explicit C64 artifacts such as `.prg`, `.d64`, maps, screenshots, and test logs;
3. validate first in an emulator;
4. optionally transfer to real hardware after emulator evidence is good;
5. capture what was learned back into the Workbench.

## Boundary

The LLM may assist with 6502/6510 assembly, BASIC V2, cc65 C, memory maps, sprite/charset planning, build scripts, debugging hypotheses, and documentation.

The repo remains the custody layer. It must not claim emulator or hardware success unless the result is captured as evidence.

## First outcome

The first useful outcome is a reproducible "hello C64" path that can build a small `.prg`, run in an emulator, and leave a clear trace for the next session.

## First application direction

The first application direction is `C64 MEMORY PAL`: a C64 Hello Console that can grow into an ELIZA-style rule-based chatbot. A modern LLM may be used as an external host or reasoning assistant later, but the Workbench must not claim that a C64 is running an LLM natively.


## Project direction: C64 Learning Lab

The primary project direction is now `C64 Learning Lab`.

The lab loop is:

```text
concept truth -> tiny runnable program -> emulator evidence -> verifier -> Capture Back
```

The first milestone is the emulator-first learning loop: define the lab contract, create the first lab sequence, add the first three lab skeletons, document emulator review, and verify lab completeness.

The chatbot direction remains as `C64 MEMORY PAL`, but it is best treated as a later synthesis lab after screen output, keyboard input, PETSCII layout, state, and memory limits have been explored.
