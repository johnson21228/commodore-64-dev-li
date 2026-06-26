# Goal Language to Assembly Network Proxy Lab

Lab 011 tests whether a C64 app can be described in language and generated as assembly while following a realistic internet-connection pattern.

The lab does **not** pretend that a stock C64 performs modern HTTPS directly. Instead, it uses a vintage-computer network split:

```text
C64 assembly app
  -> RS232/Hayes modem stream
  -> host proxy/server
  -> modern TCP/HTTP/TLS work
```

The C64 artifact remains assembly-only:

```text
goal.lang -> program.lang -> generated_intent.json -> generated.s -> .prg
```

No `main.c` may be generated or consumed.

## Optimization posture

Runtime speed and small machine-facing code are allowed to outrank teaching clarity. The generated app uses direct screen memory writes and KERNAL RS232 calls rather than a C runtime or high-level library.

## Network boundary

The C64-generated app owns:

- screen setup,
- RS232 device open,
- Hayes-style command transmission,
- one-line response reading,
- display of the proxy response.

The host proxy owns:

- TCP listener for VICE/adapter,
- modem-like `OK` / `CONNECT` behavior,
- internet/TLS/HTTP translation in later versions.
