# Capture Back: P03 WASD Solid Active Box Wireframe

The solid-active box diagnostic proved the active bitmap path is real and visible, but the active block read as a large white slab.

This patch keeps the compact solid-active box payload and adds a coarse black wireframe by changing the runtime cell fill pattern: top/bottom active box rows are cleared and left/right active box columns clear one bit, leaving black cuts around each placed cube box.

This is still a diagnostic step. It preserves speed and payload size while making the block boundaries visible before moving to face-accurate fills.
