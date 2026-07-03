# Capture Back — Pac-Man Progression to Assembly LI

## Captured decision

Lab 010 should progress to assembly through explicit intermediate contracts.

The source board image and language files define intent. They are not enough to generate trusted game assembly directly.

The board must be defined first. Then that verified board can be used with additional LI to generate rendering, movement, dot eating, scoring, ghosts, and increasingly real game outcomes.

## Lab

`labs/010_goal_language_to_asm_pacman_bounce`

## Current source input

The canonical source board image lives at:

`labs/010_goal_language_to_asm_pacman_bounce/assets/source_board.png`

This image is visual input. It is not runtime authority.

The current source image should be treated as a reference screenshot to project into a C64-feasible board model. It is not assumed to already satisfy C64 graphics constraints.

## Progression rule

Lab 010 must not jump directly from source image or vague language to full game assembly.

The required progression is:

1. source input
2. board definition
3. board verification
4. board-only C64 render
5. Pac-Man movement over the verified board
6. dot eating
7. score / completion
8. ghosts / collision / loss
9. increasingly authentic game behavior

Assembly is generated only after the relevant LI contract exists and the board data is verified.

Generated assembly is an artifact derived from board data and behavior LI. It is not the long-term source of truth.

## Milestone A — Board projection contract

Define the board before runtime behavior.

Expected artifacts:

- `src/board.txt`
- `src/projected_board.json`
- board verifier

The board contract must define:

- board bounds
- walls
- traversable paths
- dots
- power dots if present
- Pac-Man start if present
- ghost starts if present
- outside / non-playable cells
- best-fit adjustments from the source image to the C64-feasible grid

The verifier must prove dimensions, allowed symbols, traversability, walls, dots, and movement reachability.

## Milestone B — Board render

The first C64 runtime milestone should render only the board:

- walls
- dots
- empty traversable paths
- outside / non-playable area if represented

No Pac-Man behavior is required in this milestone.

This milestone proves that the projected board model can become visible C64 output.

## Milestone C — Pac-Man random dot eater

After board rendering works, add Pac-Man.

The first Pac-Man behavior may be simple/random.

Rules:

- Pac-Man starts on a traversable path cell.
- Pac-Man chooses only legal moves.
- Pac-Man does not enter walls.
- Pac-Man does not enter outside / non-playable cells.
- Pac-Man consumes dots from the same board model used for rendering and collision.

This milestone proves that movement, collision, and dot eating share the same board authority.

## Milestone D — Simple game loop

After Pac-Man can move and eat dots, add simple game outcomes:

- score increases when dots are eaten
- eaten dots disappear
- completion condition when all dots are eaten or all reachable dots are eaten
- restart behavior if needed

## Milestone E — Ghosts and real game outcomes

After the simple dot-eating loop works, add increasingly real Pac-Man-style behavior:

- ghost start cells
- ghost movement
- ghost collision
- loss / restart behavior
- lives if needed
- more authentic timing and game rhythm

## Authority chain

The authority chain is:

1. source board image
2. goal language / program language
3. projection LI
4. projected board data
5. behavior LI
6. generated C64 board data
7. generated assembly
8. C64 runtime behavior

## Workbench / LI principle

Language and image define intent.

LI defines the contracts.

Data proves the board.

Assembly is generated from verified contracts.

Runtime review checks the projection.

## Important direction

Do not keep hidden hand-authored maze rows inside an assembly template as the long-term authority.

`generate_asm.py` should eventually read projected board data such as `board.txt` or `projected_board.json`.

The existing embedded maze may remain temporarily as prototype data, but it is not the desired long-term authority.

## Scope of this Capture Back

This Capture Back records the progression rule and milestone order.

It does not implement the milestones.

It does not change `generate_asm.py`.

It does not attempt computer vision.
