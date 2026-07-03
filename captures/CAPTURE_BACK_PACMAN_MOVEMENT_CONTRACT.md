# Capture Back — Pac-Man Movement Contract

## Captured correction

The Lab 010 Pac-Man movement target is continuous Pac-Man-style movement with buffered turn requests.

Pac-Man should not auto-turn at hallway ends.

## Correct behavior

Pac-Man continues in his current direction while legal.

Player input records a requested direction.

At a legal turn point:

1. Turn if the requested direction is legal.
2. Otherwise continue current direction if legal.
3. Otherwise stop at the cell center.

## Why this matters

The auto-turn slice made Pac-Man keep moving, but it violated the intended game behavior.

The right fix is not auto-turning.

The right fix is reliable buffered input.

If VICE joystick mapping is unreliable, add a C64 keyboard fallback that writes into the same requested-direction buffer.

## Lab direction

Future Lab 010 movement work should implement:

- continuous current-direction momentum
- requested-direction buffering
- legal-turn application at board-cell centers
- no automatic turn selection
- optional keyboard fallback for VICE arrow/key input
