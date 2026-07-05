# Capture Back — Four Ghost Actor Model Hold

## Captured direction

Move the Pac-Man lab toward a fuller ghost model where ghosts are actors from the start, even before they are released into the maze.

## Original Pac-Man reference

Original Pac-Man has four ghosts:

- Blinky / red
- Pinky / pink
- Inky / cyan
- Clyde / orange

The arcade behavior is not that ghosts spawn later from nowhere. The ghosts exist as part of the board state. Some begin in the ghost house and are released into the maze according to release rules.

Original Pac-Man is more complex than this lab needs right now. It includes ghost house rules, dot counters, release timing, chase/scatter behavior, frightened behavior, and individual ghost targeting personalities.

## Workbench interpretation

This lab should be arcade-inspired, not arcade-exact.

Proposed rule:

Ghosts are actors from the start. Captive ghosts use house pacing; released ghosts use maze movement. Release changes state; it does not create the ghost.

## Proposed actor states

- captive
- exiting
- released

Captive ghosts:

- start inside the ghost house
- visibly pace inside the house
- do not yet use full maze pathing
- do not collide with Pac-Man unless a later slice explicitly supports that

Released ghosts:

- use the F.10 smooth target-cell movement model
- choose legal maze movement
- participate in collision with Pac-Man

Exiting ghosts:

- transition from house pacing to maze movement
- may use a simple fixed exit path before full release

## Why this matters

This gives the game full actor participation early without pretending to implement full arcade ghost intelligence.

The player can see that the ghost house is alive. The maze becomes more dangerous as ghosts are released. This is more coherent than adding ghosts later as if they were spawned.

## C64 sprite implication

Four ghost bodies plus Pac-Man requires five hardware sprites:

- Sprite 0: Pac-Man
- Sprite 1: ghost 1
- Sprite 2: ghost 2
- Sprite 3: ghost 3
- Sprite 4: ghost 4

This fits within the C64 hardware sprite limit of eight.

However, separate eye overlay sprites for all four ghosts would likely exceed the sprite budget. Therefore, if four ghosts are prioritized, eyes should be simplified, baked into ghost sprites, deferred, or applied only as a later targeted slice.

## Proposed implementation path

F.11 Four ghost actor model

- define four ghost identities
- define four ghost state slots
- preserve current one-ghost movement behavior as the first released ghost
- keep other ghosts captive/deferred if needed
- update generated intent to describe four actors
- update verifier to protect actor count and state model

F.12 Captive house pacing

- all captive ghosts visibly move back and forth inside the ghost house
- released ghosts continue to use F.10 smooth maze movement

F.13 Ghost release schedule

- release ghosts one at a time
- release rule may be timer-based or dot-count-based
- release changes state from captive to exiting to released

F.14 Personality-lite

- add simple distinct movement preferences or targeting hints
- remain arcade-inspired, not arcade-exact

## Deferred

- arcade-exact release counters
- full chase/scatter modes
- frightened mode
- ghost eyes for all ghosts
- individual original Pac-Man targeting algorithms

## Hold status

This is a repo hold, not an implementation commitment.

The key Workbench point:

Represent ghosts as persistent actors with state, not as later-created objects.
