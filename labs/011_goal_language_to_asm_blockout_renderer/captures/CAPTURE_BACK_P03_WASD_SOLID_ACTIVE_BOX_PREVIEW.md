# Capture Back: P03 WASD Solid Active Box Preview

The active-only diagnostic proved the endpoint active renderer only draws tiny wire marks even without the pit.

This patch adds a separate diagnostic target instead of mutating the known-good endpoint preview.

New target: `p03_elbow_wasd_3x3x10_pit_solid_active_preview.prg`.

The new builder uses `placedCells` from the 108 orientation/cursor pose payloads and emits compact active box payloads: count plus `row0,row1,col0,col1` per placed cube.

The C64 runtime clears the bitmap, draws the green dotted pit, then fills the active 8x8 screen-cell boxes white. This is intentionally coarse and fast enough to prove visible solid active-block behavior before face-accurate fills.
