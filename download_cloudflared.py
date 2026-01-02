
import requests
import os

url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
filename = "cloudflared.exe"

print(f"Downloading {filename} from {url}...")
try:
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print("Download complete.")
except Exception as e:
    print(f"Error downloading: {e}")
