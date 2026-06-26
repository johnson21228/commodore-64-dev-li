# Lab 011 — Goal Language to Assembly Network Proxy Ping

Lab 011 asks whether a C64 app can be described in language and generated as assembly while using an internet-style connection pattern.

The answer in this lab is deliberately bounded:

```text
goal.lang
  -> program.lang
  -> generated_intent.json
  -> generated.s
  -> c64net_proxy_ping.prg
```

There is no `src/main.c`. The generated C64 app is assembly.

## Network pattern

A stock C64 does not own modern internet concerns such as HTTPS/TLS. Lab 011 uses the practical vintage-computer pattern:

```text
C64 generated assembly app
  -> KERNAL RS232 device 2
  -> VICE RS232-over-IP or real WiFi modem
  -> host-side modem/proxy server
  -> modern internet/TCP/HTTP/TLS boundary
```

The C64 side sends a tiny Hayes-style script:

```text
AT
ATDT127.0.0.1:6464
GET /c64/ping
```

The host proxy responds with short ASCII lines. The C64 reads one line at a time and displays the final response on screen.

## Run shape

Terminal 1:

```bash
cd /Users/stevejohnson/Developer/commodore-64-dev-li
make lab011-server
```

Terminal 2:

```bash
cd /Users/stevejohnson/Developer/commodore-64-dev-li
make lab011
make lab011-run-net
```

The server listens on `127.0.0.1:25232`. VICE is configured to connect emulated C64 userport RS232 to that listener.

## Goal-language contract

The goal describes the app:

```text
goal "C64NET PROXY PING"
priority runtime speed first
output assembly
constraint no main.c
constraint generated assembly is the app
network pattern modem proxy server
requires host proxy server
requires RS232 or WiFi modem bridge
request line "GET /c64/ping"
show proxy response on screen
```

The implementation language commits the C64-side shape:

```text
implements goal "C64NET PROXY PING"
optimize for speed
open rs232 device 2 config 1200 8n1
dial proxy "127.0.0.1:6464" using hayes
send line "GET /c64/ping"
read response line to row 15 col 2 max 36
loop forever
```

## Expected evidence

- `generated_intent.json` records the goal and program meaning.
- `generated.s` contains KERNAL RS232 calls and no C dependency.
- `c64net_proxy_ping.prg` builds through `cl65`.
- With the host proxy running, the VICE/C64 app sends the AT script and displays `C64NET PONG ...`.
