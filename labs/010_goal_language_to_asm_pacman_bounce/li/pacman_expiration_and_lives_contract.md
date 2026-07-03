# Pac-Man Expiration and Lives Contract

## Rule model

A game has multiple Pac-Man lives.

Pac-Man expiration is the smaller primitive. Lives are the accounting around that primitive.

## Expiration

Pac-Man can enter an expiration state.

Expiration is a controlled state transition, not an immediate reset.

During expiration:

- Pac-Man movement stops.
- Player input is ignored.
- Score remains unchanged.
- Already-consumed dots remain consumed.
- The board is not restarted.
- After a short timeout, Pac-Man resets to the start cell if lives remain.

## Lives

Lives are game-level accounting.

Initial lives: 3.

Each Pac-Man expiration consumes one life.

If lives remain:

- Pac-Man resets to the start cell.
- Requested direction buffer is cleared.
- Normal play resumes.

If no lives remain:

- The game enters game-over state.
- Movement stays stopped.
- Input does not resume play until a future restart/new-game rule exists.

## Temporary trigger

Until ghost collision exists, the tunnel may be used as temporary expiration scaffolding.

The tunnel is a temporary expiration trigger, not the final cause of Pac-Man death.

## Future trigger

When ghosts exist:

- Pac-Man/ghost collision triggers Pac-Man expiration.
- The lives rule does not need to know whether expiration was caused by tunnel scaffolding or ghost collision.
