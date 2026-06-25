# C64 Learning Lab Sequence

This is the recommended first sequence for the C64 Learning Lab.

## Lab 001: Hello Screen

Goal:

```text
Build and run a `.prg` in VICE.
```

Concepts:

```text
toolchain
.prg output
emulator launch
basic screen output
```

## Lab 002: Screen Memory

Goal:

```text
Write directly to C64 screen RAM.
```

Concepts:

```text
$0400 screen RAM
character bytes
40-column layout
row/column addressing
```

## Lab 003: Color Memory

Goal:

```text
Change character colors through color RAM.
```

Concepts:

```text
$D800 color RAM
foreground color
screen memory vs color memory
```

## Lab 004: PETSCII Frame

Goal:

```text
Draw a simple PETSCII frame or mascot.
```

Concepts:

```text
character graphics
retro UI layout
PETSCII visual language
```

## Lab 005: Keyboard Input

Goal:

```text
Read typed input into a small command loop.
```

Concepts:

```text
input handling
command parsing
state
```

## Lab 006: Sprite Pet

Goal:

```text
Display and move a sprite face or pet.
```

Concepts:

```text
sprite data
sprite registers
x/y position
sprite color
animation
```

## Lab 007: SID Mood Machine

Goal:

```text
Make the C64 produce simple sound effects.
```

Concepts:

```text
SID voices
waveforms
frequency
envelope
sound as feedback
```

## Lab 008: Memory Pal

Goal:

```text
Build a tiny rule-based chatbot / assistant.
```

Concepts:

```text
text input
keyword matching
small memory table
personality
screen UX
```

## Lab 009: Online Gateway

Goal:

```text
Send a short message to a local server and display a short response.
```

Concepts:

```text
C64 as terminal
REST gateway boundary
network adapter path
LLM bridge architecture
```

## Rule for adding labs

Add labs in a way that preserves the learning ladder. Every lab should make one C64 machine concept visible.


## Runnable Lab 002 checkpoint

Lab 002 Screen Memory is now runnable. It writes directly to `$0400`, shows Lab 002 explanatory text, and marks `SCREEN[0]` with a red `A` as the visible proof.

Root shortcuts:

```bash
make lab002
make lab002-run
```
