# Lab 010 LI — Assembly Efficiency Contract

## Purpose

The learning surface is language and LI.

Under the hood, generated assembly should be compact, reviewable, and C64-respectful.

The user should learn through:

- `goal.lang`
- `program.lang`
- LI contracts
- generated intent
- visible runtime review

The generated assembly should not stay intentionally wasteful just because it is generated.

## Renderer rule

The board renderer should use a table-driven board renderer.

Unrolled per-cell board writes are superseded for Lab 010.

## Current E.1 renderer

E.1 uses compact board render character rows generated from `board.txt`.

Blank cells are skipped because `clear_screen` already initialized the screen and color RAM to black blank cells.

Color is derived from the compact character value:

- wall glyphs use blue
- dot and power-dot glyphs use yellow

## Authority boundary

Efficiency must not change board authority, movement authority, or sprite projection authority.

Board authority remains:

- `src/board.txt`
- `src/projected_board.json`

Movement authority remains:

- `li/pacman_movement_contract.md`

Sprite projection authority remains:

- `li/sprite_projection_contract.md`

## Efficiency rule

Prefer compact runtime tables and loops when they preserve the language-level intent.

Do not expose unnecessary assembly verbosity as the teaching surface.

Generated assembly should be efficient gold under a language-centered learning surface.
