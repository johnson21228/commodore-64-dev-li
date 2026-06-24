# C64 Toolchain Options

This Workbench starts with several plausible toolchain paths. Pick one per experiment.

## Path A: cc65 C-first

Best for a first reproducible path if the goal is to learn the build/run loop with a small program.

Typical artifact: `.prg`.

Evidence to capture:

- `cc65`, `cl65`, or package version output;
- exact compile command;
- emulator command;
- observed screen result.

## Path B: Kick Assembler assembly-first

Best for learning 6510/6502 assembly, sprites, raster work, charsets, and demo-style workflows.

Typical artifact: `.prg`.

Evidence to capture:

- Java version if relevant;
- Kick Assembler version;
- exact assembly command;
- emulator result.

## Path C: BASIC V2 first

Best for nostalgia and immediate machine-level feel. BASIC programs can be source-captured as text and converted to loadable formats later.

Evidence to capture:

- source listing;
- conversion/load path;
- emulator/hardware behavior.

## Path D: C64 Studio IDE

Best when using a Windows IDE-centered flow for project organization, graphics tools, debugging support, and game-focused assembly/BASIC workflows.

Evidence to capture:

- project file layout;
- export format;
- emulator integration settings;
- screenshots of successful run.

## Current default recommendation

For the first Workbench session, use cc65 + VICE if installed or easy to install. If not, start with a source-only design and capture setup as the first task.
