# Capture Back — Ghost Speed Tuning Hold

## Captured request

Consider a small follow-on slice to increase ghost speed by about 10% after F.10 smooth ghost movement.

## Current implementation

F.10 smooth ghost movement uses an integer pixel tick:

`GHOST_PIXEL_SPEED_TICKS = $04`

This means the ghost advances one pixel after the configured tick interval.

## Important constraint

A simple constant change cannot represent a 10% increase accurately.

Changing `$04` to `$03` would make the ghost substantially faster, roughly a 33% tick-interval reduction, not a 10% tuning.

## Better implementation direction

If the desired change is truly around 10%, use a fractional or accumulator-style speed model rather than replacing `$04` with `$03`.

Conceptual model:

`ghost_speed_accumulator += 11`
`if ghost_speed_accumulator >= 40: move ghost one pixel and subtract 40`

That gives an average interval of about 40 / 11 = 3.636 frames per pixel.

Compared with the current 4 frames per pixel, this is about 10% faster.

## Proposed slice

F.10.1 Ghost speed tuning

Scope:

- preserve F.10 smooth target-cell movement
- preserve legal movement
- preserve collision behavior
- add ghost speed accumulator
- tune speed to approximately 10% faster
- update generated_intent.json to declare the speed model
- update verifier to protect the tuning
- visually confirm in VICE

Deferred:

- ghost walking animation
- ghost eyes
- targeting
- multiple ghosts

## Hold status

This is a small tuning hold, not yet an implementation commitment.

The key Workbench point:

A numeric tuning request should be translated into an explicit runtime model before changing constants.
