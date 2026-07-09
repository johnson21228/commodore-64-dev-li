# Capture Back: Visible Green 3x3x10 Pit Diagnostic

## Finding from previous pit-only screenshot

The pit was technically green, but only a short top/opening region was readable. The full pit was not visually proven.

## Diagnostic change

This PRG keeps active block drawing disabled and uses an explicit enlarged screen projection:

```text
pit:
  3x3x10
  large top opening grid
  side-wall rails
  depth rings every two levels

block:
  skipped
```

## Expected visual result

A clearly readable green wire pit should appear. If this does not appear, the issue is not block overwrite; it is pit projection or bitmap/color setup.
