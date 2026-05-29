import subprocess, time, os, re

DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(DIR)

# Kill old processes
subprocess.run("taskkill /F /IM cloudflared.exe", shell=True, capture_output=True)

# Kill anything on port 8080
result = subprocess.run("netstat -ano | findstr :8080", shell=True, capture_output=True, text=True)
for line in result.stdout.splitlines():
    if "LISTENING" in line:
        pid = line.strip().split()[-1]
        subprocess.run(f"taskkill /F /PID {pid}", shell=True, capture_output=True)

time.sleep(2)

# Start HTTP server in background
subprocess.Popen(
    ["python", "-m", "http.server", "8080", "--directory", DIR],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)

time.sleep(1)
print(f"HTTP server started on port 8080")

# Start cloudflared
proc = subprocess.Popen(
    ["cloudflared.exe", "tunnel", "--url", "http://localhost:8080"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

url_found = False
for line in proc.stdout:
    print(line.rstrip())
    m = re.search(r"(https://[a-z0-9-]+\.trycloudflare\.com)", line)
    if m and not url_found:
        url = m.group(1)
        url_found = True
        print()
        print("=" * 60)
        print(f"PUBLIC URL: {url}")
        print(f"MAIN PAGE:  {url}")
        print(f"DASHBOARD:  {url}/Анализ_ссылочной_массы_дашборд.html")
        print("=" * 60)
        # Keep running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            proc.terminate()