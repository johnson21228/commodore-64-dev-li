# Emulator First, Hardware Later

## Rule

Do not move directly from generated code to real-hardware claims. Validate in an emulator first unless the human explicitly chooses a hardware-first investigation.

## Why

Emulators provide repeatable startup, fast iteration, debugger/monitor support, screenshots, and easier command capture.

## Evidence to capture

For emulator validation, capture:

- emulator name and version when available;
- exact command line;
- program artifact path;
- screenshot or observed result;
- whether PAL/NTSC or machine model was specified;
- any monitor/debugger findings.

## Hardware handoff

For real hardware, capture transfer method and environment:

- disk image transfer path;
- cartridge/Ultimate/SD2IEC/pi1541/other device;
- display standard;
- keyboard/joystick setup;
- mismatch between emulator and hardware behavior.
