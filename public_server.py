import http.server
import socketserver
import threading
import os
import time

from pyngrok import ngrok

PORT = 8080
DIR = os.path.dirname(os.path.abspath(__file__))

os.chdir(DIR)

# Start HTTP server in a thread
handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), handler)
server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
server_thread.start()
print(f"HTTP server started on http://localhost:{PORT}")

# Open ngrok tunnel
public_url = ngrok.connect(PORT, "http")
print(f"\n{'='*60}")
print(f"PUBLIC URL: {public_url}")
print(f"{'='*60}")
print("Send this link to your friend!")
print("Press Ctrl+C to stop...\n")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    ngrok.kill()
    httpd.shutdown()
    print("Stopped.")