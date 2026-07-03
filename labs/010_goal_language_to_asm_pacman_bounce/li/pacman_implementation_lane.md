# Lab 010 LI — Pac-Man Implementation Lane

## Purpose

This file turns the full rule contract into staged implementation slices.

## Active baseline

Current baseline:

- D.8 buffered Pac-Man movement with W/A/S/D fallback
- E.1 compact table-driven board renderer

## Next slice: F.2 scoring

F.2 should add score accounting.

Minimum F.2 behavior:

- score starts at zero
- consuming a small dot adds 10
- consuming an energizer adds 50
- consumed cells do not score twice
- score is visible on screen
- generated intent declares scoring rules
- verifier checks scoring constants and board-derived score opportunity

Implementation should preserve:

- board authority
- movement contract
- sprite projection contract
- compact renderer

## Later slices

### F.3 round-clear accounting

Track remaining dots and energizers.

Declare round complete when all are consumed.

### F.4 energizer state

Add a simple frightened-mode timer and energizer active state.

### F.5 first ghost movement

Add one ghost using board-constrained movement.

### F.6 ghost collision

Detect collision between Pac-Man and ghost.

### F.7 full ghost modes

Add scatter/chase/frightened mode scheduler.

### F.8 individual ghost rules

Add Blinky, Pinky, Inky, and Clyde target behavior as separate rule contracts.

### F.9 fruit

Add fruit appearance and scoring.

### F.10 level progression

Add round progression and level-dependent values.

## Implementation policy

Each slice must:

- preserve current verifier coverage
- update generated intent
- update LI if the rule becomes active
- avoid large all-at-once game rewrites
- keep generated assembly efficient under the hood
