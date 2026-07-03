# Capture Back — Pac-Man Image-to-C64 Board Projection

## Captured decision

Lab 010 should restart the long-term Pac-Man board pipeline from a source board image.

The current Lab 010 prototype has a Pac-Man-like board embedded inside `generate_asm.py` / generated assembly. That may remain temporarily as prototype data, but it should not be the desired long-term source of truth.

The long-term direction is:

1. begin with a simple source board image
2. project that image into machine-readable board data
3. generate C64 board data from the projected model
4. generate assembly
5. review the result in the C64 runtime

## Lab

`labs/010_goal_language_to_asm_pacman_bounce`

## Source image asset

The source board image should live at:

`labs/010_goal_language_to_asm_pacman_bounce/assets/source_board.png`

This image is visual input. It is not runtime authority.

## Rule

A Pac-Man-style gameboard must be clearly defined before C64 runtime generation.

The source image may guide the board, but the C64 runtime must not depend on the image directly. The image must be projected into a clearly defined, machine-readable board model before assembly generation.

## Required projected board model

The projected board model must define:

- board bounds
- wall cells
- traversable path cells
- dot cells
- power-dot cells if present
- Pac-Man start cell
- ghost start cells if present
- outside / non-playable area
- legal movement graph or equivalent traversability proof
- ambiguous cells or best-fit adjustments

## Best-fit projection

Best-fit projection is allowed.

Best-fit means the workbench may approximate the source image into a C64-feasible tile or character grid, but every adjustment must be explicit and reviewable.

Examples of best-fit adjustments include:

- cropping
- padding
- grid alignment
- wall thickness approximation
- dot-to-cell assignment
- corridor alignment
- removal of visually ambiguous dots
- simplifying curved or irregular image features into tile-grid movement

## Authority chain

The authority chain is:

1. source board image
2. projection rules / projection script
3. projected board model
4. generated C64 board data
5. generated assembly
6. C64 runtime behavior

The projected board model is the contract between image understanding and C64 runtime generation.

## Runtime rule

Rendering, dot eating, wall collision, and Pac-Man movement must all use the same projected board model or generated data proven equivalent to it.

Pac-Man may only travel through cells marked traversable.

Dots may only exist on traversable cells.

Walls must block movement.

Generated assembly must be derived from the projected board model.

## Important direction

Do not keep hidden hand-authored maze rows inside an assembly template as the long-term authority.

`generate_asm.py` should eventually read projected board data such as `board.txt` or `projected_board.json`.

The existing embedded maze may remain temporarily as prototype data, but it is not the desired long-term authority.

## Scope of this Capture Back

This Capture Back records the architectural rule and adds the source board image asset.

It does not implement full image parsing.

It does not attempt computer vision.
