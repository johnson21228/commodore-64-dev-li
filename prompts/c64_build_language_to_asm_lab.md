# Prompt: Build the C64 Language-to-Assembly Lab

Use this prompt to implement or extend the controlled language layer.

Read first:

```text
li/domain/language_to_assembly_contract.md
docs/c64/language_to_assembly_layer.md
docs/c64/lab_sequence.md
li/domain/lab_artifact_contract.md
```

Task:

```text
Add or update a tiny controlled language command. The command must parse into intent JSON and emit deterministic ca65-compatible assembly. Preserve program.lang, generated_intent.json, and generated.s. Update verifier coverage. Do not claim emulator success unless VICE or hardware evidence is captured.
```

Constraints:

```text
- Unknown commands fail closed.
- Assembly is emitted by repo-owned generator code, not by direct LLM freehand.
- Generated assembly includes comments that trace back to source commands.
- Keep each lab step visible: language input, intent model, assembly, build output, emulator evidence.
```
