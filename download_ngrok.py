import urllib.request, zipfile, os

url = 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip'
zp = 'ngrok-dl.zip'
ep = 'ngrok-bin'

exe_path = os.path.join(ep, 'ngrok.exe')
if os.path.exists(exe_path):
    print(f'ngrok.exe already exists at {exe_path}')
else:
    print('Downloading ngrok...')
    urllib.request.urlretrieve(url, zp)
    print('Extracting...')
    with zipfile.ZipFile(zp, 'r') as z:
        z.extractall(ep)
    os.remove(zp)
    print(f'ngrok.exe exists: {os.path.exists(exe_path)}')