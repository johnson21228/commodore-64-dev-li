# C64 Language-to-Assembly Layer

This document defines the first LI direction for a small language layer that generates C64 assembly directly.

## Goal

Create a deterministic path from simple language statements to runnable C64 assembly.

```text
write tiny language -> parse into intent JSON -> emit ca65-compatible assembly -> build PRG -> review in VICE
```

The goal is not general natural-language programming. The first goal is a tiny, inspectable, fail-closed C64 command language.

## Why C64 is a good target

The C64 has visible machine effects at stable addresses:

```text
$0400  screen RAM
$D800  color RAM
$D020  border color
$D021  background color
```

That means a tiny command can map to short, readable assembly.

## Example command file

```text
set border blue
set background black
clear screen
put "LANGUAGE TO ASM" at row 10 col 5 color yellow
wait forever
```

## Example generated idea

```asm
lda #$06
sta $d020
lda #$00
sta $d021
```

Longer text writes are emitted as explicit stores into screen RAM and color RAM offsets.

## Lab 009

Lab 009 is the first language-to-assembly proof.

It owns:

```text
labs/009_language_to_asm/src/program.lang
labs/009_language_to_asm/src/generate_asm.py
labs/009_language_to_asm/src/generated_intent.json
labs/009_language_to_asm/src/generated.s
```

The generated assembly is intentionally checked/verified as a human-inspectable artifact after running the generator.

## Growth path

Possible later layers:

```text
Lab 010: language labels and gotos
Lab 011: language-driven keyboard branches
Lab 012: language-driven sprite setup
Lab 013: language-driven SID tone setup
Lab 014: Memory Pal script language
```

Each growth step should add only one machine concept.
