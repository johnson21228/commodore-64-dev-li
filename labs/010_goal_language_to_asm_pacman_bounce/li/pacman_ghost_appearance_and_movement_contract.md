# Pac-Man Ghost Appearance and Movement Contract

## Purpose

This contract defines ghosts as playfield objects, not merely sprite art.

A ghost is a visible moving hazard that belongs to the active playfield.

## Core distinction

Ghost location answers: where is the ghost?

Ghost appearance answers: what does the ghost look like?

Ghost movement answers: what moves are legal?

Ghost targeting answers: which legal move is preferred?

Ghost animation answers: how does the ghost look alive?

Ghost collision answers: what happens when Pac-Man touches it?

## Ghost defining properties

Each ghost has:

- identity
- start location
- current location
- current direction
- speed or movement timing
- sprite appearance
- animation state
- collision behavior
- movement legality rules
- targeting rule
- reset rule
- mode or state

## Appearance rules

A ghost is rendered as a visible sprite overlay.

A ghost does not own the board cell underneath it.

A ghost does not erase or consume dots.

Pac-Man owns item consumption.

Ghosts are overlays.

The ghost body may have one or more sprite frames.

Walking animation is appearance only. It does not decide movement.

Eyes are appearance and direction indicators. They do not decide targeting.

## Movement rules

A ghost occupies a board cell.

A ghost may also have an in-between sprite pixel position while moving from one cell to the next.

A ghost moves cell-to-cell through traversable board cells.

A ghost cannot pass through walls.

A ghost cannot leave the declared playfield topology.

A ghost chooses a new direction only at cell centers.

A ghost avoids reversing direction unless blocked or a later mode rule requires reversal.

Movement changes the ghost's board position.

Animation changes the ghost's visual frame.

Targeting selects a preferred legal direction.

## Collision rules

A dangerous ghost collision triggers Pac-Man expiration.

Pac-Man expiration consumes one life.

If lives remain, Pac-Man resets to his start.

Ghost reset behavior is explicit and separate from Pac-Man reset behavior.

## Reset rules

Ghosts appear at playfield start.

A ghost starts at its declared start location.

For the current one-life/active-playfield slice, a ghost remains active until Pac-Man expires, game over occurs, or a future round reset rule exists.

After Pac-Man expiration, if lives remain, ghosts return to their declared start locations.

Consumed dots do not reset when a life is lost.

## Game, round, and life boundary

A life is one Pac-Man attempt within the current board state.

A round is a board-clearing attempt with dots and energizers.

The game is the sequence of lives and rounds until game over.

Ghosts should be defined for one active playfield and one Pac-Man life before full round structure is added.

## Implementation sequence

F.7 Ghost contract cleanup

- define ghost properties in LI
- make generated intent expose ghost identity, start, current state, appearance, collision, and deferred movement/animation/targeting

F.8 Ghost reset after Pac-Man expiration

- ghost returns to start when Pac-Man loses a life and lives remain
- consumed dots remain consumed

F.9 Ghost legal movement

- one ghost moves through traversable cells
- wall legality gates movement
- collision still triggers expiration
- ghost does not consume dots

F.10 Ghost walk animation

- body frame alternates while moving
- bottom changes visually to suggest walking or floating
- movement authority remains board-cell logic

F.11 Ghost eye direction

- eyes point in current travel direction
- eyes are visual indicators only

F.12 Weighted pursuit targeting

- ghost prefers legal moves that reduce distance to Pac-Man
- movement legality still gates targeting
