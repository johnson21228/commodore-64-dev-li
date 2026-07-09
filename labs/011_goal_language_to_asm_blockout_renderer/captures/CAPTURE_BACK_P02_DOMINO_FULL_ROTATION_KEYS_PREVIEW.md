# Capture Back: P02_DOMINO Full Rotation Keys Preview

## Decision

Add an ASAP interactive rotation-key proof for the dynamic block.

This preview uses original-game-style rotation keys:

```text
A / Q -> x_axis orientation
S / W -> y_axis orientation
D / E -> z_axis orientation
```

For P02_DOMINO there are three unique axis orientations:

```text
x_axis: across x
y_axis: across y
z_axis: depth
```

## Important boundary

This is an interactive preview, not the final lean runtime.

It proves:

- the C64 can respond to rotation keys;
- the dynamic block can swap among the three unique domino orientations;
- the dashed-pit / solid-block visual grammar still works.

It does not yet prove:

- legal rotation transitions;
- collision-aware rotation;
- dirty restore;
- file I/O;
- endpoint runtime line drawing.

## Rendering grammar

```text
pit = subtle dashed white
dynamic block = solid white
```

This avoids relying on separate colors inside C64 hi-res 8x8 color cells.
