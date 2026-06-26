# Capture Back — C64 Goal Language to Assembly Network Proxy Lab

## Summary

Added Lab 011 as a language-front-end C64 app that generates assembly and follows a practical internet pattern:

```text
C64 assembly app -> RS232/Hayes stream -> host proxy/server -> modern internet boundary
```

## What changed

- Added `labs/011_goal_language_to_asm_net_proxy/`.
- Added `goal.lang` and `program.lang`.
- Added deterministic generator that emits `generated_intent.json` and `generated.s`.
- Added host-side `proxy_server.py` for VICE RS232-over-IP testing.
- Added verifier coverage.

## Important boundary

The C64 app does not perform HTTPS/TLS. The generated app talks a tiny line protocol over RS232. The host proxy/server is responsible for internet-facing work.

## Output contract

No `main.c` is generated or consumed. The app artifact is assembly:

```text
generated.s -> c64net_proxy_ping.prg
```
