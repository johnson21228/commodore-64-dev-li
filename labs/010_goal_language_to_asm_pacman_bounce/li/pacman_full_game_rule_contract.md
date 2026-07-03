# Lab 010 LI — Pac-Man Full Game Rule Contract

## Purpose

This contract defines the full-game rule target for Lab 010.

The current runtime is not expected to implement all of these rules yet.

This file gives future increments a coherent rule destination.

## Current implemented rule subset

Already implemented:

- verified board projection
- compact board renderer
- Pac-Man hardware sprite
- radial Pac-Man sprite art
- sprite projection contract
- continuous current-direction movement
- buffered requested turns
- joystick input path
- W/A/S/D keyboard fallback
- dot clearing as Pac-Man reaches cells

## Full-game rule lanes

### 1. Dot and scoring rules

Pac-Man earns points by consuming items.

Scoring targets:

- small dot: 10
- energizer: 50
- frightened ghost chain: 200, 400, 800, 1600
- fruit: level-dependent values

Lab 010 should first implement small-dot and energizer scoring from the verified board.

### 2. Round completion

A round is complete when all dot and energizer cells from the board projection have been consumed.

Lab 010 should use its projected board counts, not assume the arcade maze count.

### 3. Energizers and frightened mode

When Pac-Man consumes an energizer:

- ghosts enter frightened behavior if eligible
- frightened ghost score chain resets for that energizer
- frightened ghosts become edible for a timed interval
- eaten frightened ghosts return toward the ghost house

### 4. Ghost common movement

Ghosts move on board paths and cannot pass through walls or outside cells.

Ghosts generally choose directions at tile centers according to their current mode and target tile.

Ghosts do not simply wander randomly during chase/scatter modes.

### 5. Scatter and chase modes

Ghosts alternate between scatter and chase mode according to a level/time schedule.

Mode changes may cause ghost reversals.

### 6. Individual ghost targeting

Each ghost has a distinct targeting rule.

The implementation should model these rules as separate LI-owned rule functions before assembly generation.

### 7. Ghost house and release

Ghosts have house entry, exit, and release behavior.

This should be implemented only after scoring and basic ghost movement exist.

### 8. Collision and lives

If Pac-Man collides with a dangerous ghost, Pac-Man loses a life.

If Pac-Man collides with a frightened edible ghost, the ghost is eaten and score is awarded.

### 9. Fruit

Fruit appears under defined conditions and awards level-dependent points when eaten.

### 10. Level progression

After all dots are cleared, the next round begins.

Future level progression can adjust speed, frightened duration, and fruit values.

## Out of scope for early slices

The following should not be implemented before scoring and basic ghost rule lanes are stable:

- exact arcade timing tables
- kill screen behavior
- perfect-score implementation
- full ghost house fidelity
- fruit timing precision
- attract mode
- sound
- full arcade ROM equivalence

## Rule authority

This file is the full-game rule destination.

Implementation slices should update the increment ledger and verifier as rules become active.

Generated assembly remains an artifact.
