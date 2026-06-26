#!/usr/bin/env python3
"""Tiny host-side modem/proxy for Lab 011.

This is not C64 app code. It is the modern server/proxy side of the lab.
VICE connects its emulated RS232 device to this TCP listener. The generated C64
assembly talks as if it were using a Hayes-style modem stream.
"""
from __future__ import annotations

import socket
import sys
from datetime import datetime, timezone

HOST = "127.0.0.1"
PORT = 25232


def send_line(conn: socket.socket, text: str) -> None:
    conn.sendall((text + "\r\n").encode("ascii", errors="replace"))


def handle(conn: socket.socket, addr: tuple[str, int]) -> None:
    print(f"C64NET proxy accepted VICE/C64 RS232 connection from {addr}")
    send_line(conn, "C64NET PROXY READY")
    buffer = b""
    connected = False
    while True:
        data = conn.recv(1)
        if not data:
            print("C64NET proxy connection closed")
            return
        if data in (b"\r", b"\n"):
            line = buffer.decode("ascii", errors="replace").strip()
            buffer = b""
            if not line:
                continue
            print(f"C64 -> proxy: {line}")
            upper = line.upper()
            if upper == "AT":
                send_line(conn, "OK")
            elif upper.startswith("ATDT"):
                connected = True
                send_line(conn, "CONNECT 1200")
            elif connected and upper == "GET /C64/PING":
                stamp = datetime.now(timezone.utc).strftime("%H%M%SZ")
                send_line(conn, f"C64NET PONG {stamp}")
            else:
                send_line(conn, "ERROR")
        else:
            buffer += data


def main() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(1)
        print(f"C64NET proxy listening on {HOST}:{PORT}")
        print("Start Lab 011 with: make lab011-run-net")
        while True:
            conn, addr = server.accept()
            with conn:
                try:
                handle(conn, addr)
            except (ConnectionResetError, BrokenPipeError, OSError) as exc:
                print(f"C64NET proxy connection from {addr} closed/reset: {exc}")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nC64NET proxy stopped")
        raise SystemExit(130)
