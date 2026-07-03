# Lab 010 LI — Pac-Man Increment Ledger

## Purpose

This ledger records the Lab 010 Pac-Man behavior and runtime increments so future work can distinguish active direction from superseded experiments.

The current target is D.8.

## Current target

D.8 implements Pac-Man-style continuous movement with buffered player turn requests.

Runtime input paths:

- joystick port 2 at `$dc00`, when emulator/hardware mapping is valid
- W/A/S/D C64 keyboard fallback
- both write into the same requested-direction buffer

Movement rule:

1. Pac-Man continues in the current direction while the next board cell is traversable.
2. Player input buffers a requested direction.
3. At a board-cell center, the buffered requested direction is applied if legal.
4. If the buffered requested direction is blocked, Pac-Man continues current direction if legal.
5. If current direction is blocked and no legal buffered turn exists, Pac-Man stops at the cell center.
6. Pac-Man must not auto-select turns.

## Increment ledger

### C.4 — Hardware sprite interpolation

Moved Pac-Man from a character-cell marker to hardware sprite 0.

The board remains rendered as character/tile data.

### C.5 — Smaller animated sprite

Added open/closed mouth hardware sprite frames by direction.

### C.6 — Sprite copy and speed fix

Copied all 512 bytes for eight sprite frames and corrected movement speed.

### C.7 — Smaller diameter and slower mouth

Reduced visual footprint and slowed mouth animation.

### C.8 — Half-speed movement

Changed movement to two raster frames per interpolated pixel.

### C.9 — Faster mouth crunch

Kept C.8 movement speed while increasing mouth toggle cadence.

### C.10 — Dedicated vertical sprite art

Experimented with hand-authored north/south sprite art.

### C.11 — Equal-footprint sprite art

Constrained all sprite directions to a shared visual footprint.

### C.12 — Radial sprite geometry

Generated all directions from one radial Pac-Man pixel model.

### C.13 — Y-origin tuning

Lowered hardware sprite Y origin by one pixel.

### C.14 — X-origin tuning

Shifted hardware sprite X origin left by one pixel.

### C.15 — X-origin retuning and projection contract

Shifted hardware sprite X origin left two additional pixels and captured the board-coordinate versus sprite-projection distinction.

Current sprite projection:

    return 17 + (left + x) * 8
    return 44 + (top + y) * 8

### D.1 — Joystick-controlled movement experiment

Introduced joystick port 2 as an input source.

Superseded direct movement semantics with buffered-turn semantics in D.7.

### D.2 — BASIC autostart header

Added a BASIC `10 SYS 2061` autostart line.

### D.3 — PRG load address

Restored the required two-byte C64 PRG load address `$0801`.

### D.4 — Continuous momentum

Introduced current-direction momentum and turn requests.

### D.5 — Starting momentum

Initialized Pac-Man with an immediate legal first target so motion begins without waiting for input.

### D.6 — Auto-turn experiment

Superseded.

D.6 made Pac-Man auto-select a turn when blocked. That kept Pac-Man moving, but it was not canonical Pac-Man behavior and is no longer valid for this lab.

### D.7 — Buffered requested turns

Removed auto-turning and implemented the movement contract.

Input updates a requested-direction buffer. Pac-Man applies that buffered turn only when legal at a board-cell center.

### D.8 — W/A/S/D keyboard fallback

Added C64 keyboard fallback into the same requested-direction buffer used by joystick input.

Keys:

- W = up
- A = left
- S = down
- D = right

D.8 avoids depending on VICE joystick mapping for the first playable control test.

## Superseded behavior

The runtime must not contain or regenerate auto-turn routines such as:

    auto_turn_from_blocked_momentum

Auto-turning is not the target behavior.


### E.1 — Table-driven board renderer

Replaced unrolled per-cell board rendering with compact board render character rows and a row/column loop.

This preserves the language/LI learning surface while making generated assembly smaller and more C64-respectful.

E.1 also removes embedded audit-only `board_row_*` data from generated assembly. Board audit authority remains in `src/board.txt` and `src/projected_board.json`.
