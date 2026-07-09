# Capture Back: P03 WASD Arrow Translation Verifier Contract Tolerance

The arrow-translation report generator preserved the correct WASD_3x3x10 contract, but the rewritten verifier expected exact field spellings for `anchor` and `pitDimensions`.

This verifier repair keeps the same contract checks while accepting the report's actual field shape. It verifies the active piece remains inside the current 3x3x10 pit, has 12 orientations, uses 28 endpoint line segments per pose, and exposes A/Q/S/W/D/E rotation plus cursor-arrow translation.
