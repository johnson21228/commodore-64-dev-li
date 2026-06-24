# C64 Emulator Review Workflow

## Purpose

The emulator is the first review surface for C64 Learning Lab work.

## Default review posture

For every lab:

```text
build -> run in VICE -> observe -> capture evidence -> Capture Back
```

## Evidence to capture

Capture at least one of:

```text
build command and output
VICE launch command
screenshot
short observation note
known mismatch or limitation
```

## Review questions

Ask:

```text
Did the `.prg` build?
Did it launch in the emulator?
Did the screen/sound/input behavior match `expected.md`?
Was anything emulator-specific?
Is the claim limited to emulator evidence, not real hardware?
```

## Real hardware boundary

Do not claim real C64 hardware success from emulator evidence. Real hardware has its own evidence requirement.

## Recommended local command shape

Use explicit paths in terminal snippets:

```bash
cd /Users/stevejohnson/Developer/commodore-64-dev-li/labs/001_hello_screen
make
x64sc dist/hello_screen.prg
```

The exact emulator command may vary by local VICE installation.
