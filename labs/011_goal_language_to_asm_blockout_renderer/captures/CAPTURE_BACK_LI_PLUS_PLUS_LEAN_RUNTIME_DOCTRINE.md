# Capture Back: LI++ Lean Runtime Doctrine

## Decision

Lab 011 should treat the C64 as a lean deterministic executor, not as the reasoning surface.

The C64 memory limit is not just a constraint. It defines the architecture:

```text
The intelligence lives upstream.
The runtime stays lean.
The payload is the contract.
The screen is the proof.
```

## LI++ meaning

LI++ means Language Infrastructure, not just prose documentation.

This capture is intended to become machine-checkable infrastructure:

- doctrine text;
- structured source contract;
- verifier;
- runtime boundary;
- generator responsibility list;
- memory-budget rule;
- source-to-payload rule.

The Workbench/LI side carries meaning and invariants. The generator transforms that meaning into compact artifacts. The C64 runtime executes those artifacts.

## Rule: do not put meaning in runtime if it can be compiled into data

The runtime should not know what an L piece is in a rich semantic way.

Instead, the runtime should know:

```text
current payload has:
  pose records
  occupied cells
  draw records
  dirty records
```

Shape meaning lives in LI/source and generated payloads.

## Three-layer boundary

```text
Source / LI:
  declarative, expressive, inspectable, verified

Generator:
  computational, expansive, allowed to use modern CPU/memory

C64 runtime:
  compact, byte-oriented, table-driven, disposable state
```

## Runtime as tiny interpreter

The C64 runtime interprets prepared payload instructions:

```text
RESTORE previous dirty list
CHECK candidate occupied cells
DRAW bitmap byte/mask records
SET color cells
LOCK occupied cells
LOAD/COPY next payload
```

The payload is the current piece's program. The runtime is the small machine that executes it.

## Resident memory rule

Resident memory must earn its rent.

Resident memory should be limited to data that is:

- needed every frame;
- needed for immediate input response;
- needed as current static truth;
- impossible or too slow to reload for current interaction.

Everything else should be generated, compressed, loaded on demand, recomputed off-machine, or discarded after use.

## Runtime doctrine

```text
1. Active piece is the only dynamic piece.
2. Locked world is cells, not pieces.
3. Static layer is rebuildable from pit + locked cells.
4. Piece visual data is generated offline.
5. Runtime holds one current piece payload.
6. Runtime never derives projection or masks.
7. Runtime records state as small indices and pointers.
8. Runtime favors table selection over calculation.
9. File I/O is a memory strategy, not an afterthought.
10. Verifiers protect the source-to-payload contract.
```

## Workbench mapping

```text
LI/source:
  states intent and invariants

generator:
  transforms intent into executable artifacts

verifier:
  proves the artifact matches intent

C64 PRG:
  performs only minimum mechanical behavior
```

## Architectural phrase

```text
The C64 does not reason about Blockout.
The Workbench reasons Blockout into payloads.
The C64 executes the payloads.
```
