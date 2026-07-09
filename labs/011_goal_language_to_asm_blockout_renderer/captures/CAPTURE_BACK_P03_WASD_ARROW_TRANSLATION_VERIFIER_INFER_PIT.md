# Capture Back: P03 WASD Arrow Translation Verifier Infer Pit

The report no longer carries explicit `pitDimensions` fields, but its projection contract is `WASD_3x3x10`.

This verifier repair resolves the pit contract from `projectionContract` when explicit pit dimension fields are absent, while still checking all placed cells stay inside the current 3x3x10 pit.
