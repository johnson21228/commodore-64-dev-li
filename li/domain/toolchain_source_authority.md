# C64 Toolchain Source Authority

## Rule

Toolchain facts must come from current project documentation, local installed tool output, or human-provided evidence.

## Initial toolchain families

The Workbench recognizes these starter families:

- cc65 for C and 6502-family cross-development;
- VICE for C64 emulation and emulator-first validation;
- Kick Assembler for 6510/6502 assembly workflows;
- C64 Studio for Windows-oriented IDE workflows.

## Authority order

1. Local installed tool output and successful commands in this repo.
2. Official project documentation or project repository.
3. Curated source notes in `source/c64/`.
4. Human-pasted terminal output or screenshots.
5. LLM interpretation.

## Install caution

Do not write install instructions as permanent truth unless they are dated, sourced, and/or verified locally.
