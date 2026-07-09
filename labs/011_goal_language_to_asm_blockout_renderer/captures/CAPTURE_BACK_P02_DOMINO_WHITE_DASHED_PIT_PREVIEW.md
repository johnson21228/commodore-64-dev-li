# Capture Back: P02_DOMINO White Dashed Pit Preview

## Decision

Try the C64-native color strategy:

```text
pit:
  white subtle dashed lines

dynamic block:
  solid white outline

background:
  black
```

This avoids the C64 hi-res 8x8 color-cell conflict by not relying on color to distinguish the pit from the active block.

## Why

The prior green-pit / white-block preview showed that active-block color cells can turn pit pixels white.

That means color is not a reliable distinction inside shared 8x8 cells.

The new test uses a single foreground color and differentiates by line style:

```text
dashed = static pit/reference grid
solid = active dynamic block
```

## Scope

Preview only:

- no movement;
- no dirty restore;
- no runtime line drawing;
- no lock/fill behavior;
- no file I/O.
