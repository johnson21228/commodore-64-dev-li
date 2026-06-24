# First Session: C64 Hello World

## Goal

Create a minimal, reproducible path from source to C64-visible output.

## Default choice

Use `examples/hello-cc65/hello.c` if cc65 is available. Otherwise, use this document to capture what is missing.

## Expected loop

```text
read C64 domain LI
choose toolchain
check installed versions
build small .prg
run in emulator
capture result
Capture Back durable learning
```

## Setup evidence to capture

```bash
which cl65 || true
cl65 --version || true
which x64sc || true
x64sc -version || true
```

Use the actual installed emulator command if it differs.

## Build evidence to capture

From `examples/hello-cc65/`:

```bash
make
```

Expected output path:

```text
build/hello.prg
```

## Run evidence to capture

A common VICE command shape is:

```bash
x64sc -autostart build/hello.prg
```

Do not treat this as successful until the human observes the emulator result.

## Capture Back candidate

After the run, use:

```text
prompts/c64_capture_back_dev_session.md
```
