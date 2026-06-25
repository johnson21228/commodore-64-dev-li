# C64 Language-to-Assembly Contract

The language-to-assembly layer is a deterministic C64 authoring layer, not an unconstrained natural-language compiler.

## Purpose

The layer exists to let a human or LLM write a tiny controlled language and then produce inspectable 6502/6510 assembly for a C64 program.

The required custody chain is:

```text
language command text -> parsed intent model -> generated assembly -> .prg build -> emulator evidence -> Capture Back
```

## Authority boundary

The controlled language is source input.

The parsed intent model is intermediate evidence.

The generated assembly is generated source and must remain inspectable.

The `.prg` and emulator screenshots/logs are evidence only.

A lab must not claim success merely because assembly was generated. Success requires build and emulator or hardware observation.

## First command surface

The first supported commands should stay tiny:

```text
clear screen
set border <color>
set background <color>
put "TEXT" at row <0-24> col <0-39> color <color>
wait forever
wait for key
```

The first implementation may reject every other sentence.

## Required generated artifacts

A promoted language-to-assembly lab must preserve:

```text
src/program.lang
src/generated_intent.json
src/generated.s
```

The `.lang` file records the human-facing command surface.
The intent JSON records parser custody.
The assembly records the machine-facing output.

## LLM role

An LLM may propose command text and explain assembly patterns.

An LLM must not be treated as the compiler authority. The repo-owned parser/generator and verifier decide what commands are accepted and what assembly is emitted.

## Failure posture

Unknown commands must fail closed.

Out-of-range rows, columns, and text spans must fail closed.

Unsupported colors must fail closed.

Generated assembly must include enough comments to trace each emitted block back to the original command.
