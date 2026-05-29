import http.server
import socketserver
import threading
import subprocess
import os
import time

PORT = 8080
DIR = os.path.dirname(os.path.abspath(__file__))

os.chdir(DIR)

# Start HTTP server in a thread
handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), handler)
server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
server_thread.start()
print(f"HTTP server started on http://localhost:{PORT}")

# Start ngrok
ngrok_path = os.path.join(DIR, "ngrok-bin", "ngrok.exe")
if not os.path.exists(ngrok_path):
    print(f"ngrok.exe not found at {ngrok_path}")
    print("Trying to download...")
    import urllib.request, zipfile
    url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip"
    zip_path = os.path.join(DIR, "ngrok-dl.zip")
    urllib.request.urlretrieve(url, zip_path)
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(os.path.join(DIR, "ngrok-bin"))
    os.remove(zip_path)
    print("Downloaded and extracted ngrok")

print(f"Starting ngrok tunnel on port {PORT}...")
proc = subprocess.Popen(
    [ngrok_path, "http", str(PORT)],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)

# Wait for ngrok to start and print URL
time.sleep(3)
try:
    import urllib.request
    resp = urllib.request.urlopen("http://127.0.0.1:4040/api/tunnels")
    import json
    data = json.loads(resp.read())
    for tunnel in data.get("tunnels", []):
        public_url = tunnel.get("public_url", "")
        if public_url:
            print(f"\n{'='*60}")
            print(f"PUBLIC URL: {public_url}")
            print(f"{'='*60}")
            print("Send this link to your friend!")
            break
except Exception as e:
    print(f"Could not get ngrok URL: {e}")
    print("Check http://127.0.0.1:4040 for the URL")

print("\nPress Ctrl+C to stop...")
try:
    proc.wait()
except KeyboardInterrupt:
    proc.terminate()
    httpd.shutdown()
    print("Stopped.")