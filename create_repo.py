import urllib.request
import json

import os
TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPO_NAME = "analiz-dashboard"

data = json.dumps({
    "name": REPO_NAME,
    "private": False,
    "auto_init": False
}).encode()

req = urllib.request.Request(
    "https://api.github.com/user/repos",
    data=data,
    headers={
        "Authorization": "token " + TOKEN,
        "Accept": "application/vnd.github.v3+json"
    },
    method="POST"
)
try:
    resp = urllib.request.urlopen(req)
    r = json.loads(resp.read())
    print("CREATED:", r["html_url"])
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print("ERROR", e.code, body)