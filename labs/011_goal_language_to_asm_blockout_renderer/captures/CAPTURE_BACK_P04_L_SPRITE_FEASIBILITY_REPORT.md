# Capture Back: P04_L Sprite Feasibility Report

## Question

Can the active block be drawn as white sprites over a green bitmap pit?

And can long stretches use repeated sprite motifs or corner sprites?

## Decision

Generate a feasibility report before building a sprite-overlay runtime.

The report measures the existing `P04_L` four-state visual rotation preview against standard C64 sprite limits:

```text
sprite size: 24x21 pixels
sprite bytes: 64
hardware sprites: 8
```

## Key idea

Do not start with one sprite per cube edge.

A cube has 12 edges, and a block has many projected/exposed edges. That exceeds the eight hardware sprite limit immediately.

The better first model is:

```text
active block projected outline
  -> white pixel mask
  -> 24x21 sprite tiles
  -> C64 places those tiles over the green bitmap pit
```

## Reuse hypothesis

Reusable sprite primitives may still help later:

```text
long straight stretch:
  repeated line-fragment sprite

corner/junction:
  reusable corner motif sprite
```

But those should be mined after generating actual pose masks, because perspective projection creates several slopes and lengths.

## Scope

This report does not yet build sprite runtime. It answers whether a sprite-overlay runtime is plausible.
