# Capture Back: P03 WASD Arrow Translation Verifier Repair

The arrow-translation payload and PRG rebuilt, but the report verifier had been malformed during earlier patching and referenced `REPORT` before defining it.

This replaces the report and preview verifiers with explicit checks for the current contract: `P03_ELBOW`, `WASD_3x3x10`, centered 3x3 anchor, green dotted pit, A/Q/S/W/D/E rotation, and cursor-arrow translation payloads.
