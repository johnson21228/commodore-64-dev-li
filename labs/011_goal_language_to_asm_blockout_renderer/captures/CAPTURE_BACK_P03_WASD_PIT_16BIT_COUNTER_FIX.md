# Capture Back: P03 WASD Pit 16-bit Counter Fix

The P03 WASD pit has 2126 compact pit records, but the copied preview used a one-byte pit counter and drew only 78 records.

This patch changes only the static pit-record draw loop to a 16-bit counter. Endpoint line counts stay one-byte because each active block orientation has a small line count.
