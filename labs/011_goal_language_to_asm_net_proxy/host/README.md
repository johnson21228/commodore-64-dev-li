# Lab 011 Host Proxy

`proxy_server.py` is the modern host/server side for the C64 network lab. It is intentionally not part of the C64 app.

It listens for VICE RS232-over-IP on `127.0.0.1:25232` and emulates enough Hayes/modem behavior for Lab 011:

```text
AT                    -> OK
ATDT127.0.0.1:6464    -> CONNECT 1200
GET /c64/ping         -> C64NET PONG HHMMSSZ
```

Run it before `make lab011-run-net`.
