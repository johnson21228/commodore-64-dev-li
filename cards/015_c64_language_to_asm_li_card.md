# Card 015: C64 Language-to-Assembly LI

## Intent

Introduce a controlled language layer that generates assembly directly while preserving Workbench custody.

## Decision

The layer is deterministic and fail-closed:

```text
language command text -> parsed intent JSON -> generated assembly -> PRG build -> emulator evidence
```

## First lab

```text
labs/009_language_to_asm/
```

The first lab supports screen/background/color/text commands and emits ca65-compatible assembly.

## Guardrail

The LLM may propose command language, but generated assembly is only authoritative when produced by the repo-owned generator and verified through build/evidence.
