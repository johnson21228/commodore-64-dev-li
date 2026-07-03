# Lab 010 LI — Pac-Man Rule Source Inventory

## Purpose

This file records the public rule corpus that should inform full-game Pac-Man LI.

The goal is not to copy source text.

The goal is to create a paraphrased, implementation-ready rule contract.

## Primary source anchors

### The Pac-Man Dossier

Use for:

- tile-centered movement
- pre-turn / buffered-turn behavior
- ghost movement rules
- ghost target tiles
- scatter mode
- chase mode
- frightened mode
- mode-change reversals
- speed and timing concepts
- tunnel behavior
- level behavior

### Pac-Man scoring references

Use for:

- dot score
- energizer score
- frightened ghost scoring chain
- fruit values
- perfect-score context

Canonical scoring values to model when appropriate:

- small dot: 10 points
- energizer: 50 points
- frightened ghosts in one energizer chain: 200, 400, 800, 1600
- fruit values: 100, 300, 500, 700, 1000, 2000, 3000, 5000 depending on level/fruit

### Player-facing rules and arcade references

Use for:

- maze objective
- clearing dots to complete a round
- avoiding ghosts
- lives
- fruit appearance
- tunnels
- high-level round progression

## Lab-specific caution

The original arcade maze has canonical dot counts and exact timings.

Lab 010 uses its own projected board.

Therefore, scoring and completion rules should use Lab 010 board authority:

- `src/board.txt`
- `src/projected_board.json`

When Lab 010 dot counts differ from arcade Pac-Man, the lab should preserve the Pac-Man scoring values but use the lab board's verified dot counts.

## Source-use policy

- Paraphrase.
- Preserve rule meaning.
- Do not paste long source excerpts.
- Keep exact implementation claims inside LI contracts.
- Implement in small verified slices.
