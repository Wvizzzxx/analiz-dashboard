import http.server, socketserver, threading, os, subprocess, re, time

PORT = 8080
DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(DIR)

# Start HTTP server
handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), handler)
server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
server_thread.start()
print(f"Server started on port {PORT}")

# Start cloudflared
proc = subprocess.Popen(
    ["cloudflared.exe", "tunnel", "--url", f"http://localhost:{PORT}"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

url_found = False
with open("PUBLIC_URL.txt", "w") as f:
    for line in proc.stdout:
        print(line.rstrip())
        m = re.search(r"(https://[a-z0-9-]+\.trycloudflare\.com)", line)
        if m and not url_found:
            url = m.group(1)
            f.write(url)
            f.flush()
            url_found = True
            print()
            print("=" * 60)
            print(f"PUBLIC URL: {url}")
            print("=" * 60)

if not url_found:
    print("Waiting for URL...")
    time.sleep(5)
    # Try reading from proc again
    try:
        import urllib.request
        resp = urllib.request.urlopen("http://127.0.0.1:4040/api/tunnels")
    except:
        pass

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    proc.terminate()
    httpd.shutdown()