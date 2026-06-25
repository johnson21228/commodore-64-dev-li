# Capture Back: C64 Language-to-Assembly LI

## Change

Added LI for a deterministic language-to-assembly layer.

## Why

The C64 Learning Lab can now grow beyond hand-written examples into a constrained authoring layer where simple language commands generate inspectable 6502/6510 assembly.

## Custody chain

```text
program.lang -> generated_intent.json -> generated.s -> language_to_asm.prg -> emulator evidence
```

## Boundary

This is not a general natural-language compiler. Unknown commands fail closed. The repo-owned parser/generator emits assembly. Emulator or hardware observation is still required before claiming success.

## Files

```text
li/domain/language_to_assembly_contract.md
docs/c64/language_to_assembly_layer.md
prompts/c64_build_language_to_asm_lab.md
prompts/c64_language_to_asm_capture_back.md
labs/009_language_to_asm/
tools/verify_c64_language_to_asm.py
```
