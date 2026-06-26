# Expected Result

Lab 010 should generate assembly evidence for a Pac-Man style sprite that bounces around the screen.

Expected invariant:

- the sprite moves by a signed `dx/dy` vector
- it bounces by changing `dx` and/or `dy`
- the mouth alternates open and closed
- open-mouth frames face the current vector direction
- cardinal and diagonal direction names are represented: `E`, `NE`, `N`, `NW`, `W`, `SW`, `S`, `SE`
- the lab does not reduce mouth direction to only left/right

Expected optimization:

- direction is cached in `direction_index`
- direction is recomputed only after a bounce changes velocity
- mouth pointer writes are gated by `mouth_dirty`
- sprite frame selection uses `mouth_pointer_table_01,x`
- generated assembly has exactly one `sta SPRITE_POINTER_0` write site
