#!/usr/bin/env python3
"""
Download sample animated weather GIFs for the weather app.
Each weather code gets a demo animated GIF as {code}.gif in the 'icons/' directory.
"""
import os
import requests

# List of standard OpenWeatherMap icon codes
ICON_CODES = [
    '01d', '01n', '02d', '02n', '03d', '03n', '04d', '04n',
    '09d', '09n', '10d', '10n', '11d', '11n', '13d', '13n', '50d', '50n'
]

# Public domain sample animated GIF (spinning sun)
SAMPLE_GIF_URL = "https://upload.wikimedia.org/wikipedia/commons/2/2c/Rotating_earth_%28large%29.gif"
# You can replace this with any other public domain animated GIF URL

ICON_DIR = "icons"
os.makedirs(ICON_DIR, exist_ok=True)

def download_sample_gif(code):
    filename = f"{code}.gif"
    path = os.path.join(ICON_DIR, filename)
    try:
        resp = requests.get(SAMPLE_GIF_URL, timeout=10)
        resp.raise_for_status()
        with open(path, 'wb') as f:
            f.write(resp.content)
        print(f"Downloaded {filename}")
        return True
    except Exception as e:
        print(f"Failed to download {filename}: {e}")
        return False

def main():
    print("🌤️ Downloading sample animated GIFs for all weather codes...")
    print(f"Saving to: {ICON_DIR}/")
    print("You can later replace these with real weather GIFs if desired.")
    
    for code in ICON_CODES:
        download_sample_gif(code)
    print("\n✅ Download complete!")
    print("You can now run the weather app with animated icons (demo GIF for all codes).")

if __name__ == "__main__":
    main() 