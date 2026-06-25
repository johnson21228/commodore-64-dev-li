# Capture Back: C64 First Curriculum Batch

## Date

2026-06-25

## Summary

This capture adds the next C64 Learning Lab examples after Hello Screen, Screen Memory, and Color Memory.

The new labs are:

```text
Lab 004 PETSCII UI
Lab 005 Keyboard Input
Lab 006 Sprite Basics
Lab 007 SID Tone
Lab 008 Memory Pal
```

## Why this matters

The Workbench now has a coherent first curriculum:

```text
output -> screen memory -> color memory -> text UI -> input -> sprite -> sound -> tiny app
```

## Governance

The labs remain emulator-first and toolchain-backed. Each lab has source, README, expected output, and root Makefile build/run shortcuts.

## Follow-up

A future cleanup capture should remove generated `.prg` and `.o` artifacts from Git history or, at minimum, prevent future packing/committing of generated lab outputs unless explicitly captured as evidence.
