# SID Tone App

Lab 007 introduces the SID as memory-mapped sound registers.

The program writes frequency, envelope, waveform, gate, and volume registers to produce one tone.

Core idea:

```text
Sound is register state.
The C64 does not play audio files; it drives a synthesizer chip.
```
