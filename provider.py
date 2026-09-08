import requests
import logging
import re
from datetime import datetime

SOURCE_URL = "https://raw.githubusercontent.com/sportlive18/jio-tv-auto-update-playlist/main/Sport.m3u"
OUTPUT_FILE = "stv5.m3u"
LOG_FILE = "stv5.log"

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def download(url):
    try:
        logging.info(f"Starting download: {url}")
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        logging.info("Download successful")
        return r.text
    except requests.RequestException as e:
        logging.error(f"Download failed: {e}")
        return ""

def clean_line(line: str) -> str:
    # Remove group-title attribute if present
    return re.sub(r'\s*group-title="[^"]+"', '', line, flags=re.IGNORECASE)

def main():
    logging.info("=== Scraper run started ===")
    source = download(SOURCE_URL)

    if not source:
        logging.warning("No content downloaded, exiting.")
        return

    cleaned_lines = []
    for line in source.splitlines():
        if line.startswith("#EXTINF"):
            line = clean_line(line)
        cleaned_lines.append(line)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(cleaned_lines))

    logging.info(f"Playlist saved to {OUTPUT_FILE}")
    logging.info("=== Scraper run finished ===")

if __name__ == "__main__":
    main()
