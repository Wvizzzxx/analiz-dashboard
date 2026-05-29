import http.server
import socketserver
import threading
import subprocess
import os
import time
import re

PORT = 8080
DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(DIR)

# Start HTTP server
handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), handler)
server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
server_thread.start()
print(f"HTTP server started on http://localhost:{PORT}")

# Start cloudflared
print("Starting cloudflared tunnel...")
proc = subprocess.Popen(
    [os.path.join(DIR, "cloudflared.exe"), "tunnel", "--url", f"http://localhost:{PORT}"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)

# Read output and find URL
for line in proc.stdout:
    print(line.rstrip())
    match = re.search(r'(https://[a-z0-9-]+\.trycloudflare\.com)', line)
    if match:
        url = match.group(1)
        print(f"\n{'='*60}")
        print(f"PUBLIC URL: {url}")
        print(f"{'='*60}")
        print("Send this link to your friend!")
        break

try:
    proc.wait()
except KeyboardInterrupt:
    proc.terminate()
    httpd.shutdown()