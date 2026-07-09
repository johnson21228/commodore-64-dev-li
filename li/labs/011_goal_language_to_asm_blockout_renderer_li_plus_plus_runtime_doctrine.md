# Lab 011 LI++: Lean Runtime Doctrine

## Purpose

This LI++ note captures the Language Infrastructure doctrine for the C64 Blockout renderer.

The goal is not merely to describe implementation choices. The goal is to make the architecture explicit enough that future source files, generators, verifiers, and PRG builds can be checked against it.

## Core doctrine

```text
The intelligence lives upstream.
The runtime stays lean.
The payload is the contract.
The screen is the proof.
```

## Runtime posture

The C64 runtime is a small deterministic executor.

It should execute prepared payload records, not derive high-level meaning.

Allowed runtime work:

- setup display memory;
- draw or restore static pit/locked layer;
- load/copy the current active piece payload;
- select pose records;
- restore previous dirty records;
- draw current bitmap byte/mask records;
- test candidate occupied cells against locked occupancy;
- lock active cubes into occupied cells.

Disallowed runtime work:

- 3D rotation matrix math;
- projection math;
- active-piece line rasterization;
- bitmap mask discovery;
- all-shapes resident pose-table storage;
- semantic shape interpretation.

## Meaning boundary

Meaning belongs upstream:

```text
LI/source:
  what a piece means
  what rotation means
  what pose means
  what lock means
  what memory discipline means

generator:
  computes expensive records

runtime:
  executes current records
```

## Memory discipline

A byte in resident memory must earn its rent.

Prefer one active payload slot over all-shapes resident tables.

Prefer current indices and pointers over rich objects.

Prefer cell occupancy over locked piece objects.

Prefer generated records over runtime derivation.

## LI++ testable consequence

Future verifiers should be able to reject changes that:

- put all starter piece payloads resident by default;
- add runtime projection for active pieces;
- model locked blocks as locked piece objects;
- make sprites the primary active-piece renderer;
- remove the one-current-payload memory boundary;
- bypass source/verifier/payload discipline.
