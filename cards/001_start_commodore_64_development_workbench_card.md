# Card 001: Start Commodore 64 Development Workbench

## Intent

Create a domain Workbench for Commodore 64 development from the Workbench LI template.

## Added domain spine

- C64 cross-development model.
- Emulator-first validation rule.
- Toolchain source authority rule.
- C64 constraints map.
- First-session hello-world guide.
- Toolchain options guide.
- Starter prompts for project interview, hello world, visual experiments, and Capture Back.

## Initial default

Use a modern-host cross-development loop and validate with an emulator before claiming hardware behavior.

## Evidence standard

Generated source and build scripts are not success. Success requires build output plus emulator or hardware observation captured by the human.

## Verification

`tools/verify_c64_workbench.py` checks that the C64 domain layer exists and that the Makefile runs it through `make verify`.
