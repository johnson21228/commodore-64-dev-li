# Capture Back: P03 WASD Arrow Translation Preview Verifier Tolerance

The report verifier now accepts the `WASD_3x3x10` projection contract as the pit authority. The preview verifier still expected exact legacy anchor text and required translation controls specifically in metadata.

This repair keeps the real checks: P03 preview, 12 orientations, dotted pit records, orientation+cursor payload size, PRG fits, and cursor-arrow translation recorded in either report or metadata.
