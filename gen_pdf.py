# -*- coding: utf-8 -*-
import subprocess
import os

DIR = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(DIR, "Анализ_ссылочной_массы_дашборд.html")
PDF = os.path.join(DIR, "Анализ_ссылочной_массы_дашборд.pdf")

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# file:// URL
url = "file:///" + HTML.replace("\\", "/").replace(" ", "%20")

cmd = [
    CHROME,
    "--headless",
    "--disable-gpu",
    "--no-sandbox",
    "--print-to-pdf=" + PDF,
    "--print-to-pdf-no-header",
    "--virtual-time-budget=5000",
    url
]

print("Generating PDF...")
print("CMD:", " ".join(cmd))
result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
print("Return code:", result.returncode)
if os.path.exists(PDF):
    size = os.path.getsize(PDF)
    print(f"PDF created: {PDF}")
    print(f"Size: {size} bytes ({size//1024} KB)")
else:
    print("PDF NOT created!")
    print("stderr:", result.stderr[:500] if result.stderr else "empty")