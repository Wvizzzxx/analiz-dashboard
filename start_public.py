import subprocess, time, os, sys, urllib.request

DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(DIR)
NGROK = os.path.join(DIR, "ngrok-bin", "ngrok.exe")
CF = os.path.join(DIR, "cloudflared.exe")

print("Killing old processes...")
subprocess.run("taskkill /F /IM cloudflared.exe", shell=True, capture_output=True)
subprocess.run("taskkill /F /IM ngrok.exe", shell=True, capture_output=True)
time.sleep(3)

print("Starting HTTP server on port 9999...")
server = subprocess.Popen(
    [sys.executable, "-m", "http.server", "9999"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
time.sleep(3)

# Test server
try:
    r = urllib.request.urlopen("http://127.0.0.1:9999/", timeout=5)
    print(f"Server OK: HTTP {r.status}")
except Exception as e:
    print(f"Server FAIL: {e}")
    sys.exit(1)

print("Starting cloudflared tunnel...")
proc = subprocess.Popen(
    [CF, "tunnel", "--url", "http://127.0.0.1:9999"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
)

import re
for line in proc.stdout:
    print(line.rstrip())
    m = re.search(r"(https://[a-z0-9-]+\.trycloudflare\.com)", line)
    if m:
        url = m.group(1)
        print()
        print("=" * 60)
        print(f"  OPEN THIS IN BROWSER:")
        print(f"  {url}")
        print(f"  Dashboard: {url}/Анализ_ссылочной_массы_дашборд.html")
        print("=" * 60)
        with open("PUBLIC_URL.txt", "w") as f:
            f.write(url)
        break

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    proc.terminate()
    server.terminate()