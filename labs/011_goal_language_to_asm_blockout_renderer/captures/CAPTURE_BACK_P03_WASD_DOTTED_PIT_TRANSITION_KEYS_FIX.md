# Capture Back: P03 WASD Dotted Pit Transition Keys Fix

The shared-projection generator emitted transition keys as +x/-x/+y/-y/+z/-z, but the C64 preview builder consumes runtime key names A/Q/S/W/D/E.

This fixes the upstream endpoint report generator so transitions are keyed by the C64 controls while preserving the axisControls map.
