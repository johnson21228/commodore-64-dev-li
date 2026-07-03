# Lab 010 LI — Pac-Man Scoring Contract

## Purpose

F.2 adds score accounting to Lab 010.

Scoring is a board-cell consumption rule.

It is not a movement rule.

## Active F.2 scoring rules

Score starts at zero.

When Pac-Man reaches a board-cell center:

- if the cell contains an unconsumed small dot, add 10
- if the cell contains an unconsumed energizer, add 50
- otherwise, add 0

A consumed item must not score twice.

The visible dot or energizer is cleared when consumed.

## Board authority

The score opportunity comes from the Lab 010 projected board.

Board authority remains:

- `src/board.txt`
- `src/projected_board.json`

Lab 010 does not assume the arcade maze dot count.

It uses the lab board's verified counts:

- small dots: 205
- energizers: 4

## Display rule

The score should be visible on screen.

F.2 may use a simple six-digit screen-code decimal score.

Initial display:

    SCORE 000000

## Assembly rule

Generated assembly should keep scoring efficient and simple.

F.2 may use the rendered board cells as the mutable item map:

- dot glyph means unconsumed small dot
- energizer glyph means unconsumed energizer
- blank means already consumed or no item

This is valid because Pac-Man is a hardware sprite and does not overwrite the character board.

## Out of scope for F.2

- frightened ghost scoring
- fruit scoring
- extra lives
- high score table
- round completion
- sound
