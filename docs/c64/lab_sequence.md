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
Lab 009: Language to Assembly - controlled language -> intent JSON -> generated assembly
Lab 010: Pac-Mouth Vector Motion - mouth crunch follows movement vector, including cardinal and diagonal facing
```

## Next candidates

```text
Lab 011: Simple Game Loop
Lab 012: Character Set Experiment
Lab 013: Disk Save/Load Note
Lab 014: Serial/Host Gateway Sketch
```

## Lab 010: Pac-Mouth Vector Motion

Lab 010 adds a Pac-style sprite with mouth crunch behavior. The mouth opens and closes while the sprite moves, and the open-mouth frame follows the movement vector.

This lab introduces cardinal and diagonal facing behavior. The implementation stores `dx/dy` as motion truth, derives direction from that vector, and then selects the appropriate mouth frame.

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

- Lab 010: Goal Language to Pac-Man Bounce Assembly — now includes vector-facing mouth behavior from `dx_vel`/`dy_vel`.

- Lab 011: Goal Language to Network Proxy Assembly — RS232/Hayes C64 client with host proxy/server boundary.
