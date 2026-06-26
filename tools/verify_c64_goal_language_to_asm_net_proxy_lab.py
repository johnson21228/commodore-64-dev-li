#!/usr/bin/env python3
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
LAB = ROOT / "labs" / "011_goal_language_to_asm_net_proxy"

REQUIRED = {
    "docs/c64/goal_language_to_asm_net_proxy_lab.md": ["goal.lang -> program.lang", "generated.s", "No `main.c`", "RS232/Hayes", "host proxy/server"],
    "prompts/c64_build_goal_language_net_proxy_lab.md": ["goal.lang", "program.lang", "generated.s", "Do not add `src/main.c`", "host proxy/server"],
    "captures/CAPTURE_BACK_C64_GOAL_LANGUAGE_TO_ASM_NET_PROXY_LAB.md": ["RS232/Hayes", "host proxy/server", "No `main.c`", "generated.s"],
    "cards/017_c64_goal_language_to_asm_net_proxy_lab_card.md": ["goal.lang -> program.lang", "generated_intent.json", "generated.s", "Host proxy"],
    "labs/011_goal_language_to_asm_net_proxy/README.md": ["Goal Language", "generated.s", "There is no `src/main.c`", "RS232-over-IP", "C64NET PONG"],
    "labs/011_goal_language_to_asm_net_proxy/expected.md": ["C64NET PROXY PING", "C64NET PONG", "modern host proxy owns the actual internet boundary"],
    "labs/011_goal_language_to_asm_net_proxy/Makefile": ["goal.lang", "program.lang", "generated_intent.json", "generated.s", "cl65 -t c64", "proxy_server.py"],
    "labs/011_goal_language_to_asm_net_proxy/src/goal.lang": ['goal "C64NET PROXY PING"', "priority runtime speed first", "output assembly", "constraint no main.c", "network pattern modem proxy server"],
    "labs/011_goal_language_to_asm_net_proxy/src/program.lang": ['implements goal "C64NET PROXY PING"', "optimize for speed", "open rs232 device 2", "dial proxy", "send line", "read response line"],
    "labs/011_goal_language_to_asm_net_proxy/src/generate_asm.py": ["parse_goal", "parse_program", "assembly_only_no_main_c", "rs232_hayes_proxy_ping_client", "KERNAL RS232", "TEXT_PTR_LO = $fd", "lda (TEXT_PTR_LO),y"],
    "labs/011_goal_language_to_asm_net_proxy/src/generated_intent.json": ["runtime_speed_first", "assembly_only_no_main_c", "rs232_hayes_proxy_ping_client", "host_proxy_server_owns_tcp_http_tls"],
    "labs/011_goal_language_to_asm_net_proxy/src/generated.s": ["Goal: C64NET PROXY PING", "No main.c", "SETLFS = $ffba", "OPEN = $ffc0", "CHKOUT = $ffc9", "CHRIN = $ffcf", "rs232_control_name", "ATDT127.0.0.1:6464", "GET /c64/ping"],
    "labs/011_goal_language_to_asm_net_proxy/host/proxy_server.py": ["C64NET proxy", "127.0.0.1", "25232", "ATDT", "GET /C64/PING", "C64NET PONG"],
}

errors: list[str] = []
for rel, needles in REQUIRED.items():
    path = ROOT / rel
    if not path.exists():
        errors.append(f"missing {rel}")
        continue
    text = path.read_text(errors="ignore")
    for needle in needles:
        if needle not in text:
            errors.append(f"{rel} missing token {needle!r}")

if (LAB / "src" / "main.c").exists():
    errors.append("Lab 011 must not include src/main.c")

makefile = (ROOT / "Makefile").read_text(errors="ignore") if (ROOT / "Makefile").exists() else ""
for token in [
    "verify-goal-language-to-asm-net-proxy",
    "lab011",
    "lab011-run",
    "lab011-run-net",
    "lab011-server",
    "tools/verify_c64_goal_language_to_asm_net_proxy_lab.py",
    "labs/011_goal_language_to_asm_net_proxy",
]:
    if token not in makefile:
        errors.append(f"Makefile missing {token}")

sequence = (ROOT / "docs" / "c64" / "lab_sequence.md").read_text(errors="ignore") if (ROOT / "docs" / "c64" / "lab_sequence.md").exists() else ""
if "Lab 011: Goal Language to Network Proxy Assembly" not in sequence:
    errors.append("docs/c64/lab_sequence.md missing Lab 011 network proxy entry")

try:
    payload = json.loads((LAB / "src" / "generated_intent.json").read_text())
    if payload.get("optimization_posture") != "runtime_speed_first":
        errors.append("generated_intent.json missing runtime_speed_first")
    if payload.get("output_contract") != "assembly_only_no_main_c":
        errors.append("generated_intent.json missing assembly-only output contract")
    if payload.get("app_model") != "rs232_hayes_proxy_ping_client":
        errors.append("generated_intent.json missing rs232_hayes_proxy_ping_client app model")
    if payload.get("internet_boundary") != "host_proxy_server_owns_tcp_http_tls":
        errors.append("generated_intent.json missing host proxy internet boundary")
    program_ops = {item.get("op") for item in payload.get("program", [])}
    for op in ["open_rs232", "dial_proxy", "send_line", "read_response_line", "loop_forever"]:
        if op not in program_ops:
            errors.append(f"generated_intent.json missing program op {op}")
except Exception as exc:
    errors.append(f"generated_intent.json is not valid JSON: {exc}")

asm_text = (LAB / "src" / "generated.s").read_text(errors="ignore") if (LAB / "src" / "generated.s").exists() else ""
for forbidden in ["#include", "clrscr", "cputsxy", "main()", "src/main.c", "lda (text_ptr_lo),y", "text_ptr_lo:"]:
    if forbidden in asm_text:
        errors.append(f"generated.s contains forbidden C/helper token {forbidden!r}")
for required in [
    "fast_clear_loop_01:",
    "open_rs232_01:",
    "send_rs232_zstring_01:",
    "read_response_01:",
    "ascii_to_screen_01:",
    "rs232_control_name:",
    ".byte $08, $01",
    "TEXT_PTR_LO = $fd",
    "TEXT_PTR_HI = $fe",
    "lda (TEXT_PTR_LO),y",
]:
    if required not in asm_text:
        errors.append(f"generated.s missing assembly token {required!r}")
if "sta $06e8,x" in asm_text or "sta $dae8,x" in asm_text:
    errors.append("generated.s should use exact 1000-byte clear, not overlapping 256-page clear")

try:
    subprocess.run(
        [sys.executable, "src/generate_asm.py", "src/goal.lang", "src/program.lang", "src/generated_intent.json", "src/generated.s"],
        cwd=LAB,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
except Exception as exc:
    errors.append(f"Lab 011 generator failed: {exc}")

if errors:
    print("C64 Goal Language Network Proxy Lab verification failed:")
    for err in errors:
        print(f"- {err}")
    sys.exit(1)

print("OK: C64 Lab 011 goal-language front end generates RS232 proxy-client assembly only.")
