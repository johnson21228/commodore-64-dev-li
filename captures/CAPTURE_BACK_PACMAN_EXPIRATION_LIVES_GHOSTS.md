# Capture Back — Pac-Man Expiration, Lives, and Ghost LI Direction

## Context

Lab 010 is using a Pac-Man-like C64 game as a language-to-assembly learning lab.

The goal is not only to clone Pac-Man. The goal is to make game behavior explicit in LI, goal language, program language, generated intent, generated 6502 assembly, verifier checks, and visual runtime tests.

Current implemented sequence:

- Pac-Man board projection from `board.txt`
- compact generated board rendering
- hardware-sprite Pac-Man
- buffered movement
- dot and energizer scoring
- declared tunnel topology
- Pac-Man expiration state

## Current F.4 behavior

Pac-Man can expire.

The current temporary trigger is the tunnel. When Pac-Man enters the declared tunnel endpoint, the tunnel triggers Pac-Man expiration instead of being the final death cause.

This is temporary scaffolding.

Runtime behavior:

- Pac-Man enters an expiration state.
- Movement stops.
- Input is ignored.
- Pac-Man flashes/blinks.
- After a short timeout, Pac-Man resets to the start cell.
- Score remains unchanged.
- Already-consumed dots remain consumed.
- Lives are not decremented yet.

Precise language:

> Pac-Man expires, flashes, resets, and play resumes.

It is not yet technically “a life ended” because the lives counter has not been implemented.

## Lives direction

A game has multiple Pac-Man lives.

Pac-Man expiration is the smaller primitive. Lives are the accounting around that primitive.

LI rule:

- Initial lives: 3.
- Each Pac-Man expiration consumes one life.
- If lives remain, Pac-Man resets to the start cell and play resumes.
- If no lives remain, the game enters game-over state.
- Game over stops movement and input until a future restart/new-game rule exists.

## Ghost direction

Ghost rules are not yet fully defined in LI.

Current LI only says that future Pac-Man/ghost collision will trigger Pac-Man expiration. That is a collision rule, not a full ghost behavior rule.

The ghost model should be introduced in layers.

## Ghost LI concepts

Separate the ghost concept into:

1. Ghost appearance
2. Ghost board presence and collision
3. Ghost movement
4. Ghost targeting rule
5. Multiple ghost targeting personalities later

A ghost is a visible moving board-cell hazard.

Each ghost has:

- an identity
- a start cell
- a visible appearance
- a current board cell
- a current movement direction
- a targeting rule

## Ghost appearance rule

A ghost must be visible on the board as a sprite or board glyph.

Ghost appearance is separate from the board item underneath it.

A ghost moving over a dot does not consume the dot.

When the ghost leaves a cell, the underlying board cell must still be correct.

Important LI phrase:

> Pac-Man owns item consumption. Ghosts are overlays.

## Ghost collision rule

A ghost occupies a board cell.

If Pac-Man and a ghost occupy the same cell, Pac-Man expires.

The ghost collision rule triggers expiration. It does not own lives accounting.

Lives accounting remains in the game/lives rule.

## Initial ghost targeting rule

Classic Pac-Man ghosts have different targeting personalities. This lab can acknowledge that future direction while starting with a simpler targeting rule.

Initial targeting rule:

> weighted pursuit

Definition:

- Ghosts traverse legal board paths.
- Ghosts do not pass through walls.
- At decision points, a ghost chooses among legal directions.
- The ghost prefers moves that reduce Manhattan distance to Pac-Man.
- The ghost may occasionally choose a legal non-best move.
- This creates slow convergence without full pathfinding.

Manhattan distance:

    distance = abs(ghost_x - pacman_x) + abs(ghost_y - pacman_y)

This is intentionally cheaper and more explainable than full pathfinding.

## Future ghost personalities

LI can later define multiple ghost targeting rules:

- direct pursuer: tends toward Pac-Man's current cell
- ambusher: tends toward cells ahead of Pac-Man
- wanderer: mostly random, lightly weighted toward Pac-Man
- flanker: tends toward side or offset positions

These should be introduced only after one ghost can appear, collide, and move legally.

## Recommended implementation sequence

F.5 Multiple lives

- Add lives state.
- Initialize lives to 3.
- Decrement lives on expiration.
- Reset Pac-Man if lives remain.
- Enter game-over if lives reach 0.

F.6 Ghost appearance and stationary collision

- Render one ghost at a declared ghost start cell.
- Ghost does not move yet.
- Ghost is visible.
- Ghost does not consume dots.
- Pac-Man/ghost collision triggers expiration.
- Tunnel no longer needs to be the expiration trigger.

F.7 Ghost legal movement

- Ghost moves cell-to-cell.
- Ghost obeys walls.
- Ghost chooses legal directions at intersections.
- Ghost avoids reversing unless blocked.

F.8 Weighted pursuit targeting

- Legal moves are scored by Manhattan distance to Pac-Man.
- Best move is preferred.
- Occasional non-best legal move preserves randomness.
- Ghost slowly converges on Pac-Man.

F.9 Multiple ghost targeting rules

- Add differentiated ghost personalities.
- Keep each targeting rule explicit and testable.

## Core thesis for a skeptical AI developer

This Pac-Man project is not mainly about cloning Pac-Man.

It is a C64 language-to-assembly learning lab.

The interesting chain is:

    goal language
    -> program language
    -> generated intent
    -> generated 6502 assembly
    -> verifier
    -> C64 PRG
    -> visual runtime test

The C64 keeps the abstraction honest because every byte and every state transition matters.

The game is the demo. The real question is:

> Can a human describe game behavior in a small controlled language, have AI help generate efficient 6502 assembly, and keep the result explainable, verified, and incrementally teachable?
