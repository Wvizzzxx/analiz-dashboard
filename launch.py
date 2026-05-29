import subprocess, time, os, re, sys

DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(DIR)
LOG = os.path.join(DIR, "launch_log.txt")

with open(LOG, "w", encoding="utf-8") as log:
    def p(msg):
        print(msg)
        log.write(msg + "\n")
        log.flush()

    p("=== Step 1: Kill old processes ===")
    r = subprocess.run("taskkill /F /IM cloudflared.exe", shell=True, capture_output=True, text=True)
    p(f"  cloudflared: {r.stdout.strip()} {r.stderr.strip()}")
    r = subprocess.run("taskkill /F /IM ngrok.exe", shell=True, capture_output=True, text=True)
    p(f"  ngrok: {r.stdout.strip()} {r.stderr.strip()}")
    time.sleep(2)

    p("=== Step 2: Start HTTP server ===")
    server_proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", "8080"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(2)
    p(f"  HTTP server PID: {server_proc.pid}")

    try:
        import urllib.request
        resp = urllib.request.urlopen("http://localhost:8080/", timeout=3)
        p(f"  Local test: HTTP {resp.status}")
    except Exception as e:
        p(f"  Local test FAILED: {e}")

    p("=== Step 3: Start cloudflared ===")
    cf_proc = subprocess.Popen(
        ["cloudflared.exe", "tunnel", "--url", "http://localhost:8080"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    url_found = False
    for line in cf_proc.stdout:
        p(line.rstrip())
        m = re.search(r"(https://[a-z0-9-]+\.trycloudflare\.com)", line)
        if m and not url_found:
            url = m.group(1)
            url_found = True
            with open("PUBLIC_URL.txt", "w") as f:
                f.write(url)
            p("")
            p("=" * 60)
            p(f"PUBLIC URL: {url}")
            p(f"DASHBOARD:  {url}/Анализ_ссылочной_массы_дашборд.html")
            p("=" * 60)
            break

    if not url_found:
        p("URL NOT FOUND!")

    p("=== Running. Press Ctrl+C to stop. ===")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        cf_proc.terminate()
        server_proc.terminate()
        p("Stopped.")