# Card 017 — C64 Goal Language to Assembly Network Proxy Lab

## Intent

Prove that a C64 app can be described in goal/program language and generated as assembly while using a realistic network proxy pattern.

## Custody chain

```text
goal.lang -> program.lang -> generated_intent.json -> generated.s -> c64net_proxy_ping.prg
```

## Boundary

C64 owns RS232/Hayes line protocol. Host proxy owns modern internet/TCP/HTTP/TLS concerns.

## Verification

```bash
python3 tools/verify_c64_goal_language_to_asm_net_proxy_lab.py
make verify
make lab011
```
