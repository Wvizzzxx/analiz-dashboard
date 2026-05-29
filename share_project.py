# -*- coding: utf-8 -*-
"""
Запускает HTTP-сервер с правильными заголовками + Serveo туннель.
"""
import http.server
import socketserver
import threading
import subprocess
import time
import os
import re

PORT = 8080
DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(DIR)

print("=" * 60)
print("  SHARE PROJECT - Serveo Tunnel")
print("=" * 60)

class CORSHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP-сервер с правильными заголовками для браузера."""
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("X-Frame-Options", "SAMEORIGIN")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def log_message(self, format, *args):
        print(f"  [HTTP] {args[0]}")

socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(("", PORT), CORSHandler)
server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
server_thread.start()
print(f"[OK] HTTP server on http://localhost:{PORT}")

# Запускаем SSH туннель через Serveo
print(f"[...] Connecting to Serveo...")
proc = subprocess.Popen(
    [
        "ssh",
        "-o", "StrictHostKeyChecking=no",
        "-o", "ServerAliveInterval=30",
        "-o", "ServerAliveCountMax=3",
        "-R", f"80:localhost:{PORT}",
        "serveo.net"
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    encoding="utf-8",
    errors="replace"
)

url_found = False
start_time = time.time()
while time.time() - start_time < 20:
    line = proc.stdout.readline()
    if not line:
        time.sleep(0.1)
        continue
    line = line.strip()
    print(f"  [tunnel] {line}")
    # Ищем URL
    match = re.search(r'(https://[^\s]+serveousercontent\.com[^\s]*)', line)
    if match:
        url = match.group(1)
        print()
        print("=" * 60)
        print(f"  YOUR PUBLIC URL:")
        print(f"  {url}")
        print("=" * 60)
        print("  Open this link in browser and send to friend!")
        print()
        with open(os.path.join(DIR, "PUBLIC_URL.txt"), "w", encoding="utf-8") as f:
            f.write(url)
        url_found = True
        break

if not url_found:
    print("\n[WARN] Could not detect URL. Check terminal output.")

print("Press Ctrl+C to stop...\n")

try:
    proc.wait()
except KeyboardInterrupt:
    print("\nStopping...")
    proc.terminate()
    httpd.shutdown()
    print("Done.")