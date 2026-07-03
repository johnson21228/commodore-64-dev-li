# Capture Back — Pac-Man Scoring Contract

## Captured direction

F.2 adds Pac-Man scoring as a board-cell consumption rule.

When Pac-Man reaches a cell center:

- small dot adds 10
- energizer adds 50
- consumed items do not score twice
- score is visible on screen

## Boundary

Scoring should not change the movement contract.

Scoring should not change the sprite projection contract.

Scoring should not undo the compact board renderer.

## Implementation note

Because Pac-Man is a hardware sprite, the screen character board can serve as the mutable item map for F.2.

A dot or energizer screen glyph means the item is still available.

After scoring, the cell is cleared to blank.

This keeps F.2 efficient and avoids adding a second item-state table.
