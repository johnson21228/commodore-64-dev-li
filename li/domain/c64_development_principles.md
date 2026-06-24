# C64 Development Principles

## Principle 1: keep experiments small

The Workbench should favor small C64 experiments with clear evidence over large invented systems.

## Principle 2: separate language, target, and artifact

A development session must distinguish:

- source language: BASIC V2, 6502/6510 assembly, C through cc65, or another toolchain;
- target machine assumptions: PAL/NTSC, memory layout, joystick port, SID expectations, disk/tape behavior;
- output artifact: `.prg`, `.d64`, source-only example, screenshot, emulator trace, or hardware note.

## Principle 3: emulator-first, evidence-driven

The default validation path is emulator-first. The repo should capture command lines, screenshots, logs, and human observations before treating behavior as known.

## Principle 4: source authority beats LLM recall

When installing or configuring tools, check current official docs or project pages. LLM memory is not a source of truth for current tool versions, command flags, downloads, or compatibility.

## Principle 5: nostalgia does not replace constraints

C64 development is constrained by memory, CPU time, VIC-II behavior, SID behavior, keyboard/joystick input, storage format, and display standards. The Workbench should keep those constraints visible.
