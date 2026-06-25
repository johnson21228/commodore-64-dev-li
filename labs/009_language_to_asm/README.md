# Lab 009: Language to Assembly

Purpose: prove that a tiny controlled language can generate inspectable C64 assembly directly.

This is not unconstrained natural-language compilation. It is a fail-closed command language that produces ca65-compatible assembly through a repo-owned generator.

Build:

```bash
cd /Users/stevejohnson/Developer/commodore-64-dev-li
make lab009
```

Run:

```bash
cd /Users/stevejohnson/Developer/commodore-64-dev-li
make lab009-run
```

Learning point: preserve the full custody chain:

```text
src/program.lang -> src/generated_intent.json -> src/generated.s -> dist/language_to_asm.prg -> emulator evidence
```
