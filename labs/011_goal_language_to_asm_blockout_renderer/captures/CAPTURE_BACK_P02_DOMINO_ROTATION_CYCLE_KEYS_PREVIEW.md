# Capture Back: P02_DOMINO Stateful Rotation-Cycle Keys Preview

## Decision

Rotation keys must apply a rotation step, not merely select a fixed orientation.

This preview adds a stateful rotation model:

```text
A / Q -> apply x-axis rotation step
S / W -> apply y-axis rotation step
D / E -> apply z-axis rotation step
```

For the domino, the visible states are:

```text
x_axis
y_axis
z_axis
```

## Transition model

```text
x-axis rotation:
  x stays x
  y <-> z

y-axis rotation:
  y stays y
  x <-> z

z-axis rotation:
  z stays z
  x <-> y
```

## Symmetry note

A domino has only three visible axis orientations here. Directed plus/minus states collapse visually.

That means repeated presses do apply state transitions, but a domino cannot show all directed 90-degree steps the way an asymmetric block can.

Asymmetric blocks should extend this to directed orientation states.

## Rendering grammar

```text
pit = subtle dashed white
dynamic block = solid white
```

## Scope

This is still a preview:

- full frame redraw;
- no dirty restore yet;
- no collision-aware legal rotation;
- no file I/O;
- no runtime line drawing.
