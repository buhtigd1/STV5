import requests

SOURCE_URL = "https://raw.githubusercontent.com/sportlive18/jio-tv-auto-update-playlist/main/Sport.m3u"
OUTPUT_FILE = "stv5.m3u"

def download(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        return r.text
    except requests.RequestException as e:
        print(f"❌ Failed: {url}\n{e}")
        return ""

def main():
    print("Downloading playlist...")
    source = download(SOURCE_URL)

    if not source:
        print("No content downloaded.")
        return

    print("Saving playlist...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(source)

    print(f"✅ Done: saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
