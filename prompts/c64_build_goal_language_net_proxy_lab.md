# Prompt — Build C64 Goal-Language Network Proxy Lab

Use this prompt to continue Lab 011.

Goal: preserve a language-front-end C64 app whose implementation artifact is generated assembly, not `main.c`.

Required custody chain:

```text
goal.lang
  -> program.lang
  -> generated_intent.json
  -> generated.s
  -> c64net_proxy_ping.prg
```

Constraints:

- Do not add `src/main.c`.
- Do not claim the C64 owns HTTPS/TLS.
- Use the host proxy/server as the internet boundary.
- Keep RS232/Hayes behavior explicit and inspectable.
- Prefer runtime speed and machine-facing assembly over teaching clarity when there is a tradeoff.

Verification target:

```bash
python3 tools/verify_c64_goal_language_to_asm_net_proxy_lab.py
make verify
make lab011
```
