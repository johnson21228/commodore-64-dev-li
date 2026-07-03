# Lab 010 LI — Pac-Man Movement Contract

## Purpose

This contract defines the intended Pac-Man movement behavior for Lab 010.

The goal is not free-form steering, step-by-step grid movement, or auto-turning through the maze.

The goal is Pac-Man-style continuous motion with buffered turn requests.

## Canonical movement rule

Pac-Man keeps moving in his current direction while the next board cell in that direction is traversable.

Input does not push Pac-Man one step at a time.

Input records a requested direction.

At a legal turn point:

1. If the requested direction is legal, Pac-Man turns into that direction.
2. If the requested direction is not legal, Pac-Man continues in the current direction if possible.
3. If the current direction is blocked and no legal requested turn is available, Pac-Man stops at the cell center.

## No auto-turn rule

Pac-Man must not auto-select a new direction merely because he reached the end of a hallway.

Auto-turning is not the target behavior for this lab.

A direction change should come from the player's buffered input.

## Buffered input rule

A player may press or hold a direction before the exact turn point.

The runtime should preserve the most recent requested direction and apply it when that direction becomes legal.

This is the intended fix for missed turns.

## Input authority

Joystick port 2 may be used when correctly mapped by the emulator or hardware.

Because VICE keyboard-to-joystick mapping may be unreliable by default, D.8 implements a C64 W/A/S/D keyboard fallback.

The keyboard fallback updates the same requested-direction buffer as joystick input.

## Board authority

Board legality comes from:

- `src/board.txt`
- `src/projected_board.json`

The runtime may only enter traversable cells:

- `.`
- `o`
- space
- `P`
- `G`

The runtime must not enter blocked cells:

- `#`
- `X`

## Sprite projection authority

This movement contract does not replace the sprite projection contract.

Movement legality answers:

    Can Pac-Man enter this neighboring board cell?

Sprite projection answers:

    Does the visible hardware sprite sit correctly over that legal board cell?

Keep those coordinate systems separate.


## Current D.8 input implementation

D.8 reads joystick port 2 when available and also reads W/A/S/D from the C64 keyboard matrix.

Both input paths update the same requested-direction buffer.

This keeps the movement rule stable while making local VICE testing playable without joystick-map setup.
