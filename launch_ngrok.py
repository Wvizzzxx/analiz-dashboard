import subprocess, time, os, re, sys, urllib.request, json

DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(DIR)
LOG = os.path.join(DIR, "launch_log.txt")

NGROK_PATH = os.path.join(DIR, "ngrok-bin", "ngrok.exe")
AUTHTOKEN = "3EOFZe1wk05UICeoJBzRw0Ockwd_7qD35jhpHraHNW7xuSEvg"

with open(LOG, "w", encoding="utf-8") as log:
    def p(msg):
        print(msg)
        log.write(msg + "\n")
        log.flush()

    # Kill old processes
    p("=== Killing old processes ===")
    for name in ["cloudflared.exe", "ngrok.exe"]:
        subprocess.run(f"taskkill /F /IM {name}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Kill old python http.server
    r = subprocess.run("netstat -ano | findstr :8080", shell=True, capture_output=True, text=True)
    for line in r.stdout.splitlines():
        if "LISTENING" in line:
            pid = line.strip().split()[-1]
            subprocess.run(f"taskkill /F /PID {pid}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    time.sleep(2)

    # Configure ngrok authtoken
    p("=== Configuring ngrok authtoken ===")
    r = subprocess.run([NGROK_PATH, "config", "add-authtoken", AUTHTOKEN], capture_output=True, text=True)
    p(f"  {r.stdout.strip()} {r.stderr.strip()}")

    # Start HTTP server
    p("=== Starting HTTP server ===")
    server_proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", "8080"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(2)
    p(f"  Server PID: {server_proc.pid}")

    try:
        resp = urllib.request.urlopen("http://localhost:8080/", timeout=3)
        p(f"  Local test: HTTP {resp.status}")
    except Exception as e:
        p(f"  Local test FAILED: {e}")

    # Start ngrok
    p("=== Starting ngrok tunnel ===")
    ngrok_proc = subprocess.Popen(
        [NGROK_PATH, "http", "8080", "--log=stdout", "--log-format=logfmt"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    # Read ngrok output and also check API
    url_found = False

    # Wait for ngrok to start and get URL from API
    for attempt in range(20):
        time.sleep(1)
        try:
            api_resp = urllib.request.urlopen("http://127.0.0.1:4040/api/tunnels", timeout=2)
            data = json.loads(api_resp.read())
            for tunnel in data.get("tunnels", []):
                public_url = tunnel.get("public_url", "")
                if public_url and not url_found:
                    url = public_url
                    url_found = True
                    with open("PUBLIC_URL.txt", "w") as f:
                        f.write(url)
                    p(f"  TUNNEL URL: {url}")
                    break
            if url_found:
                break
        except Exception:
            pass

    if url_found:
        p("")
        p("=" * 60)
        p(f"PUBLIC URL: {url}")
        p(f"DASHBOARD:  {url}/Анализ_ссылочной_массы_дашборд.html")
        p("=" * 60)

        # Save to PUBLIC_URL.txt
        with open("PUBLIC_URL.txt", "w") as f:
            f.write(url)
    else:
        p("  Could not get URL from ngrok API. Checking logs...")
        # Read remaining ngrok output
        import select
        deadline = time.time() + 5
        while time.time() < deadline:
            try:
                line = ngrok_proc.stdout.readline()
                if line:
                    p(line.rstrip())
                    m = re.search(r"(https://[a-z0-9-]+\.ngrok[a-z0-9-]*\.app)", line)
                    if m and not url_found:
                        url = m.group(1)
                        url_found = True
                        with open("PUBLIC_URL.txt", "w") as f:
                            f.write(url)
                        p(f"PUBLIC URL: {url}")
                        break
            except:
                break

    p("=== Tunnel running. Press Ctrl+C to stop. ===")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        ngrok_proc.terminate()
        server_proc.terminate()
        p("Stopped.")