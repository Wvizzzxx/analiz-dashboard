import subprocess, time, os, sys, urllib.request, re

DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(DIR)

# Kill old processes (NOT current python)
my_pid = os.getpid()
r = subprocess.run("wmic process where name='python.exe' get ProcessId", shell=True, capture_output=True, text=True)
for line in r.stdout.splitlines():
    line = line.strip()
    if line.isdigit() and int(line) != my_pid:
        subprocess.run(f"taskkill /F /PID {line}", shell=True, capture_output=True)

subprocess.run("taskkill /F /IM cloudflared.exe", shell=True, capture_output=True)
subprocess.run("taskkill /F /IM ngrok.exe", shell=True, capture_output=True)
time.sleep(3)

PORT = 9999

# Start server
print("Starting server...")
server = subprocess.Popen(
    [sys.executable, "-m", "http.server", str(PORT)],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
time.sleep(2)

# Test
try:
    r = urllib.request.urlopen(f"http://127.0.0.1:{PORT}/", timeout=5)
    print(f"Server OK: HTTP {r.status}")
except Exception as e:
    print(f"Server FAIL: {e}")
    sys.exit(1)

# Start SSH tunnel
print("Starting SSH tunnel...")
ssh = subprocess.Popen(
    ["ssh", "-o", "StrictHostKeyChecking=no", "-R", f"80:localhost:{PORT}", "nokey@localhost.run"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
)

for line in ssh.stdout:
    print(line.rstrip())
    m = re.search(r"(https://[a-z0-9-]+\.lhr\.life)", line)
    if m:
        url = m.group(1)
        print()
        print("=" * 60)
        print(f"  YOUR PUBLIC URL: {url}")
        print(f"  Dashboard: {url}/Анализ_ссылочной_массы_дашборд.html")
        print("=" * 60)
        with open("PUBLIC_URL.txt", "w") as f:
            f.write(url)
        break

# Keep alive - restart server if it dies
try:
    while True:
        time.sleep(5)
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{PORT}/", timeout=3)
        except:
            print("Server died, restarting...")
            try:
                server.terminate()
            except:
                pass
            server = subprocess.Popen(
                [sys.executable, "-m", "http.server", str(PORT)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            time.sleep(2)
except KeyboardInterrupt:
    try:
        ssh.terminate()
    except:
        pass
    try:
        server.terminate()
    except:
        pass
    print("Stopped.")