import requests
import logging
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

def main():
    logging.info("=== Scraper run started ===")
    source = download(SOURCE_URL)

    if not source:
        logging.warning("No content downloaded, exiting.")
        return

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(source)
    logging.info(f"Playlist saved to {OUTPUT_FILE}")
    logging.info("=== Scraper run finished ===")

if __name__ == "__main__":
    main()
