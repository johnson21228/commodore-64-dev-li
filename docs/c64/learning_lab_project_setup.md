# C64 Learning Lab Project Setup

## Identity

The primary project direction for this Workbench is now:

```text
C64 Learning Lab
```

The lab is a Workbench-backed curriculum for learning Commodore 64 development by building small, verified, runnable experiments.

## Analogy to existing Workbench projects

### Bracket Builder analogy

Bracket Builder works through:

```text
data truth -> rendering/controller behavior -> verifier -> Capture Back
```

C64 Learning Lab works through:

```text
C64 concept truth -> tiny runnable program -> emulator evidence -> verifier -> Capture Back
```

A lab is like a bracket feature card: small enough to verify, visible enough to review, and captured back when done.

### Take60 analogy

Take60 has a measurement boundary:

```text
readiness -> controlled capture -> computed result -> evidence
```

C64 Learning Lab has a machine-learning boundary:

```text
machine concept -> controlled experiment -> observed behavior -> evidence
```

Example:

```text
Truth: C64 screen RAM begins at $0400.
Experiment: write a character byte to $0400.
Observed result: the top-left screen character changes.
```

### Grazing / Registry analogy

The Grazing and Registry efforts build larger systems from small canonical assets. C64 Learning Lab does the same:

```text
machine concept -> lab card -> runnable artifact -> source map -> next lab
```

## Product shape

The eventual product can become a menu-driven C64 program:

```text
C64 LEARNING LAB

1 SCREEN MEMORY
2 PETSCII
3 COLORS
4 SPRITES
5 SID SOUND
6 KEYBOARD INPUT
7 DISK SAVE/LOAD
8 MEMORY PAL
9 ONLINE GATEWAY
```

At first, each lab should be a separate `.prg`. Later, the labs may be unified into one menu shell.

## First milestone

Milestone 1 is the emulator-first learning loop:

```text
1. Define the lab artifact contract.
2. Create the first lab sequence.
3. Add folders for Hello Screen, Screen Memory, and Color Memory.
4. Add an emulator review workflow.
5. Add a verifier for lab completeness.
6. Capture this direction back into the Workbench.
```

## North star

The north star is a C64-native teaching machine:

```text
SELECT LAB 002: SCREEN MEMORY

THE C64 SCREEN BEGINS AT $0400.
PRESS SPACE TO WRITE "A" INTO $0400.

OBSERVE: THE TOP-LEFT CHARACTER CHANGES.

WHY?
BECAUSE THE VIC-II READS CHARACTER CODES FROM SCREEN RAM.
```
