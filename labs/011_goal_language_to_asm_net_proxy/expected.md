# Expected Result — Lab 011

Expected visual result in VICE:

```text
C64NET PROXY PING
LANGUAGE GENERATED ASM
NO MAIN.C
RS232 MODEM PROXY
SENDING GET /C64/PING
RESPONSE:
C64NET PONG HHMMSSZ
```

Expected host-side result:

```text
C64NET proxy listening on 127.0.0.1:25232
C64 -> proxy: AT
C64 -> proxy: ATDT127.0.0.1:6464
C64 -> proxy: GET /c64/ping
```

This lab proves the language front end can generate an assembly-only C64 app that speaks a tiny proxy protocol. The modern host proxy owns the actual internet boundary.
