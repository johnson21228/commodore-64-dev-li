# C64 Learning Lab Sequence

The C64 Learning Lab grows as a sequence of tiny runnable programs. Each lab teaches one machine concept and leaves behind a source-backed artifact.

## Current labs

```text
Lab 001: Hello Screen       - prove cc65 -> .prg -> VICE loop
Lab 002: Screen Memory      - write visible characters through $0400
Lab 003: Color Memory       - pair screen RAM with color RAM at $D800
Lab 004: PETSCII UI         - build a simple text interface
Lab 005: Keyboard Input     - read keys and update program state
Lab 006: Sprite Basics      - define, point, position, and enable sprite 0
Lab 007: SID Tone           - write sound registers for a tone
Lab 008: Memory Pal         - tiny rule-based C64 helper app
```

## Next candidates

```text
Lab 009: Moving Sprite
Lab 010: Simple Game Loop
Lab 011: Character Set Experiment
Lab 012: Disk Save/Load Note
Lab 013: Serial/Host Gateway Sketch
```

## Pattern

Each lab should include:

```text
README.md
expected.md
src/main.c or src/main.asm
Makefile
root Makefile shortcut
verifier coverage
capture/card/prompt when promoted to LI
```
