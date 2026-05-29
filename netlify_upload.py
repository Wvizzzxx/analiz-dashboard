# -*- coding: utf-8 -*-
"""
Загружает HTML-дашборд на Netlify и получает публичную ссылку.
"""
import zipfile
import urllib.request
import json
import io
import os
import glob
import shutil

DIR = os.path.dirname(os.path.abspath(__file__))

# Находим HTML файл
html_file = os.path.join(DIR, "Анализ_ссылочной_массы_дашборд.html")
if not os.path.exists(html_file):
    html_files = glob.glob(os.path.join(DIR, "*.html"))
    if html_files:
        html_file = html_files[0]
    else:
        print("ERROR: No HTML files found!")
        exit(1)

print(f"Using file: {os.path.basename(html_file)}")

# Создаём ZIP в памяти
zip_buffer = io.BytesIO()
with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.write(html_file, "index.html")
    print("Added index.html")

zip_data = zip_buffer.getvalue()
print(f"ZIP size: {len(zip_data)} bytes")

# Загружаем на Netlify
print("\nUploading to Netlify...")
try:
    req = urllib.request.Request(
        "https://api.netlify.com/api/v1/sites",
        data=zip_data,
        headers={"Content-Type": "application/zip"},
        method="POST"
    )
    resp = urllib.request.urlopen(req, timeout=30)
    data = json.loads(resp.read().decode())
    
    site_url = data.get("ssl_url") or data.get("url")
    site_name = data.get("name", "unknown")
    
    print(f"\n{'='*60}")
    print(f"DEPLOYED SUCCESSFULLY!")
    print(f"Site name: {site_name}")
    print(f"PUBLIC URL: {site_url}")
    print(f"{'='*60}")
    print("Send this link to your friend!")
    
    # Сохраняем URL
    with open(os.path.join(DIR, "PUBLIC_URL.txt"), "w", encoding="utf-8") as f:
        f.write(site_url)
        
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f"\nERROR {e.code}: {body}")
except Exception as e:
    print(f"\nERROR: {e}")