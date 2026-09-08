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
    # Remove group-title attribute
    line = re.sub(r'\s*group-title="[^"]+"', '', line, flags=re.IGNORECASE)
    # Remove decorative separator lines (lots of '=' and text in between)
    if re.match(r'^\s*=+\s*.*\s*=+\s*$', line):
        return ""  # drop the line entirely
    return line

def main():
    logging.info("=== Scraper run started ===")
    source = download(SOURCE_URL)

    if not source:
        logging.warning("No content downloaded, exiting.")
        return

    lines = source.splitlines()
    cleaned_lines = ["#EXTM3U"]  # always start with header

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("#EXTINF"):
            # Clean the EXTINF line
            extinf = clean_line(line)
            # Look ahead for the next non-comment line (the URL)
            url = ""
            j = i + 1
            while j < len(lines):
                next_line = lines[j].strip()
                if not next_line.startswith("#"):
                    url = next_line
                    break
                j += 1
            if extinf and url:
                cleaned_lines.append(extinf)
                cleaned_lines.append(url)
            i = j + 1
        else:
            i += 1

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(cleaned_lines))

    logging.info(f"Playlist saved to {OUTPUT_FILE} with {len(cleaned_lines)-1} channels")
    logging.info("=== Scraper run finished ===")

if __name__ == "__main__":
    main()
