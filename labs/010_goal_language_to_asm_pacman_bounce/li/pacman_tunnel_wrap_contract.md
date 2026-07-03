# Pac-Man Tunnel Wrap Contract

## Slice

F.3 — tunnel wrap.

## Rule

Tunnel wrap is declared topology, not boundary escape.

Pac-Man may not freely exit the board. The only off-edge transition allowed in this slice is the declared horizontal tunnel pair on board row 09.

## Declared tunnel pair

- Left endpoint: `(0, 9)`
- Right endpoint: `(27, 9)`

## Behavior

- At `(0, 9)`, moving left wraps Pac-Man to the right tunnel endpoint and continues left.
- At `(27, 9)`, moving right wraps Pac-Man to the left tunnel endpoint and continues right.
- No other board edge permits off-board movement.
- Tunnel wrap is movement topology, not scoring logic.
- Dot and energizer scoring remain cell-consumption rules.
- Future ghost movement should share this declared topology rather than adding a separate escape rule.

## Current implementation lane

The first implementation may teleport the sprite from one endpoint to the paired endpoint, then continue movement in the same direction. A later presentation refinement may add smoother tunnel-offscreen animation.
