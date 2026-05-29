import urllib.request

url = "https://feof-prostate-informed-means.trycloudflare.com/"
print(f"Testing: {url}")
try:
    r = urllib.request.urlopen(url, timeout=15)
    print(f"STATUS: {r.status}")
    print(f"CONTENT LENGTH: {len(r.read())}")
except Exception as e:
    print(f"ERROR: {e}")