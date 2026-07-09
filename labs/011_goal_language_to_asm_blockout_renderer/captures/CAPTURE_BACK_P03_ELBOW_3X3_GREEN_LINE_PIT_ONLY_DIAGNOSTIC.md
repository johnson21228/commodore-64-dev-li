# Capture Back: P03_ELBOW 3x3 Green-Line Pit-Only Diagnostic

## Question

Is the 3x3x10 pit actually being rendered as green lines before the active block draw changes screen color cells to white?

## Diagnostic

This PRG intentionally skips active block drawing.

```text
draw:
  clear bitmap
  set screen color cells green
  draw 3x3x10 pit bitmap line records

skip:
  active block endpoint draw
  active block white color-cell writes
```

## Expected visual result

The pit should be visible as green projected side-wall/opening grid lines.

If the pit is still black or missing, the bug is in pit bitmap generation or screen-color setup.

If the pit is green here but disappears in the block preview, the bug is active-block color-cell overwrite/composition.
