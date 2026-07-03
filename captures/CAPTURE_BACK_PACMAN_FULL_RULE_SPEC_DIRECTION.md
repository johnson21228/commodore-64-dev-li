# Capture Back — Pac-Man Full Rule Specification Direction

## Captured direction

Lab 010 should use the public Pac-Man rules corpus to build a full-game rule LI.

The implementation should remain staged.

The language and LI surface should describe the game rules clearly, while generated assembly can remain efficient under the hood.

## Source posture

Use public Pac-Man references as source material, especially:

- The Pac-Man Dossier for movement, ghosts, modes, target tiles, timing, and collision behavior
- Pac-Man scoring references for dot, energizer, fruit, and frightened ghost values
- arcade/player-facing guides for high-level rules and round structure

Do not paste copyrighted source text into LI.

Paraphrase into rule contracts.

## Product direction

The learning experience remains language-centered:

- `goal.lang`
- `program.lang`
- LI contracts
- generated intent
- visible runtime review

Under the hood, the generator may produce compact assembly.

## Implementation direction

Do not implement the full game at once.

Add rules in slices:

1. scoring and dot accounting
2. energizers and frightened state
3. ghost movement common rules
4. ghost house / release rules
5. scatter/chase scheduler
6. individual ghost target rules
7. collision/lives
8. fruit
9. level progression
10. speed/timing refinements

## Next slice

F.2 should be scoring.

Scoring is the right next feature because the board already contains dots and power dots, Pac-Man already clears dots, and the lab already verifies dot counts from board projection.
