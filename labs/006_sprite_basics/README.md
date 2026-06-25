# Lab 006: Sprite Basics

Purpose: introduce the C64 sprite pipeline.

This lab copies a 24x21 sprite shape into memory, points sprite 0 at it, positions it, colors it, and enables it through VIC-II registers.

Build:

```bash
cd /Users/stevejohnson/Developer/commodore-64-dev-li
make lab006
```

Run:

```bash
cd /Users/stevejohnson/Developer/commodore-64-dev-li
make lab006-run
```

Learning point: a sprite is not just an image. It is memory data plus a pointer plus VIC-II registers.
