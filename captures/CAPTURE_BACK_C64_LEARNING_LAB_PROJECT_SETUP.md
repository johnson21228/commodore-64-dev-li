# Capture Back: C64 Learning Lab Project Setup

## Context

The conversation shifted from asking for a single C64 application to recognizing the better project identity: a Learning Lab.

The Learning Lab is an analogy to existing Workbench efforts:

```text
Bracket Builder: truth -> rendering/controller -> verifier -> Capture Back
Take60: readiness -> controlled capture -> result -> evidence
Grazing/Registry: small canonical assets -> larger system
```

## Decision

The primary C64 Workbench direction is now:

```text
C64 Learning Lab
```

This means the Workbench should build small, runnable experiments that teach C64 concepts one at a time.

## Lab loop

```text
C64 concept truth -> tiny runnable program -> emulator evidence -> verifier -> Capture Back
```

## First milestone

Milestone 1 is the emulator-first learning loop:

```text
1. Learning Lab project setup doc.
2. Lab Artifact Contract.
3. Lab sequence.
4. Emulator review workflow.
5. First three lab skeletons.
6. Learning Lab verifier.
```

## First labs

```text
001 Hello Screen
002 Screen Memory
003 Color Memory
```

## Synthesis path

The chatbot remains important, but it is better treated as a later synthesis lab:

```text
Memory Pal = text input + small memory + PETSCII UX + rule-based replies
Online Gateway = C64 terminal + C64-friendly REST/LLM server boundary
```

## Boundary

The Workbench must not claim that a C64 can run a modern LLM natively. Native C64 chatbot work is rule-based. LLM work belongs on a host/server with the C64 as the retro terminal/interface.
