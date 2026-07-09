# Capture Back: P04_L True-Axis Endpoint Payload Report

## Question

Can true x/y/z `P04_L` rotation fit if the active block payload is compact endpoint/line commands instead of full bitmap byte/mask records?

## Finding

The previous full-bitmap attempt was a payload conflict:

```text
orientationCount: 24
observedProgramBytes: 43695
availablePrgImageBytes: 30719
result: CONFLICT
```

This report replaces that payload model with:

```text
orientation transition table
  + endpoint line commands per orientation
```

## Runtime contract

```text
A/Q:
  rotate about x

S/W:
  rotate about y

D/E:
  rotate about z

C64:
  orientationId + key -> nextOrientationId
  draw prepared line endpoints
```

The C64 still does not reason about Blockout geometry. Workbench generates the orientation graph and endpoint payload.
