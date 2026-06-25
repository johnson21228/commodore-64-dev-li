# Lab 007: SID Tone

Purpose: introduce the SID chip as memory-mapped sound registers.

This lab writes a simple tone to SID voice 1 and stops it when a key is pressed.

Build:

```bash
cd /Users/stevejohnson/Developer/commodore-64-dev-li
make lab007
```

Run:

```bash
cd /Users/stevejohnson/Developer/commodore-64-dev-li
make lab007-run
```

Learning point: sound on the C64 starts with register writes, not audio files.
