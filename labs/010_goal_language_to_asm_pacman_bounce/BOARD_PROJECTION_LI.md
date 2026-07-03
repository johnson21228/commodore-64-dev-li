# Board Projection LI — Lab 010 Pac-Man

## Purpose

Lab 010 begins from a source board image, but assembly must not be generated directly from the image.

The board must first be projected into reviewable data. That projected board data becomes the runtime authority for rendering, movement, collision, and dot eating.

## Source input

Canonical source image:

`assets/source_board.png`

The source image is visual input. It is not runtime authority.

## Progression to assembly

Lab 010 progresses through explicit contracts:

1. source image and language intent
2. board projection LI
3. projected board data
4. board verifier
5. board-only render
6. Pac-Man movement and dot eating
7. score / completion
8. ghosts and game outcomes
9. generated assembly
10. C64 runtime review

Assembly is generated only after the relevant LI contract exists and the board data is verified.

## Board model rule

A board must be defined as a rectangular tile grid before assembly generation.

Each cell must have exactly one base role:

- wall
- traversable path
- outside / non-playable

A traversable path cell may additionally contain:

- dot
- power dot
- Pac-Man start
- ghost start

## Text board contract

The first projected board is stored at:

`src/board.txt`

Character contract:

- `#` = wall
- `.` = dot on traversable path
- `o` = power dot on traversable path
- space = empty traversable path
- `P` = Pac-Man start on traversable path
- `G` = ghost start on traversable path
- `X` = outside / non-playable

## Machine-readable board metadata

Projection metadata is stored at:

`src/projected_board.json`

It declares:

- source image path
- board width
- board height
- tile legend
- Pac-Man start
- ghost starts
- projection status
- best-fit notes

## Movement rule

Pac-Man may move only between orthogonally adjacent traversable path cells.

Walls block movement.

Outside cells block movement.

Diagonal movement is not legal.

Wrap tunnels are only legal if explicitly declared.

## Dot rule

Dots may only exist on traversable path cells.

Dot eating must use the same board data as rendering and collision.

## Best-fit projection rule

Best-fit projection from image to C64 tile grid is allowed.

Every best-fit adjustment must be explicit and reviewable.

Examples:

- crop
- pad
- snap to grid
- wall-thickness simplification
- dot-to-cell assignment
- corridor alignment
- simplifying curved or irregular image features into tile-grid movement

## C64 projection rule

The projected board must fit C64 screen constraints.

This first manual projection uses a compact character-grid board that can later be mapped into C64 screen cells.

The grid dimensions must be declared in data, not inferred from hidden assembly rows.

## Authority chain

The authority chain is:

1. source board image
2. projection LI / projection rules
3. projected board model
4. generated C64 board data
5. generated assembly
6. C64 runtime behavior

The projected board model is the contract between image understanding and C64 runtime generation.

## Current milestone

Milestone A: board projection contract.

This slice does not require assembly generation.

This slice does not require Pac-Man movement.

This slice does not require computer vision.
