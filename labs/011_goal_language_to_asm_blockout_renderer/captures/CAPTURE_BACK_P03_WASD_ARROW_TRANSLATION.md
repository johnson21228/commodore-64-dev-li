# Capture Back: P03 WASD Arrow Translation

The corpus confirms A/Q, S/W, and D/E as original-game-style rotation controls. This patch keeps those controls and adds C64 cursor-key translation for the active P03 block:

```text
cursor left  $9D -> x - 1
cursor right $1D -> x + 1
cursor up    $91 -> y - 1
cursor down  $11 -> y + 1
```

Workbench now emits orientation+cursor pose payloads. The runtime remains lean: it updates ORIENT/XPOS/YPOS, computes `orientationId*9 + cursorY*3 + cursorX`, and draws the precomputed endpoint payload.
