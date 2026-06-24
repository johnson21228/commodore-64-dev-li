# C64 Cross-Development Model

## Default model

This Workbench assumes a modern-host cross-development loop:

```text
edit source -> build C64 artifact -> run in emulator -> inspect behavior -> capture evidence -> revise
```

## Host side

The host can be macOS, Linux, or Windows. Host scripts should be explicit and should not assume installed tools unless captured in a setup note.

## Target side

The target is Commodore 64 compatible runtime behavior. Treat C64, C64C, Ultimate-style FPGA devices, emulators, PAL, and NTSC as related but not identical targets.

## Artifact side

Common artifacts:

- `.prg` for directly loadable programs;
- `.d64` for disk images;
- symbol/map files for debugging;
- screenshots or videos for visual evidence;
- emulator logs or monitor transcripts for debugging evidence.

## Good session shape

A good session ends with one of:

- a tested artifact and evidence;
- a failed attempt with captured commands and symptoms;
- a design note that narrows the next experiment.
