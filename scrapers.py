import re
import time
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150 Safari/537.36"
    ),
    "Accept-Language": "da-DK,da;q=0.9,en;q=0.8",
}

PRICE_RE = re.compile(r"(\d{1,3}(?:[.\s]\d{3})+|\d{4,6})\s*(?:kr\.?|DKK)", re.I)
SIZE_RE = re.compile(r"(\d{2,3}(?:[,.]\d+)?)\s*m(?:²|2)", re.I)
ROOM_RE = re.compile(r"(\d+(?:[,.]\d+)?)\s*(?:vær\.?|værelser?|rooms?)", re.I)

def fetch(url: str) -> str:
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    time.sleep(0.7)  # Be polite; do not hammer public pages.
    return r.text

def norm_num(s: str) -> float:
    s = s.replace(" ", "").replace(".", "").replace(",", ".")
    return float(s)

def extract_price(text: str):
    m = PRICE_RE.search(text)
    return int(norm_num(m.group(1))) if m else None

def extract_size(text: str):
    m = SIZE_RE.search(text)
    return norm_num(m.group(1)) if m else None

def extract_rooms(text: str):
    m = ROOM_RE.search(text)
    return norm_num(m.group(1)) if m else None

def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

def candidate_card(anchor):
    # Walk up a few levels and select the smallest ancestor containing both
    # a price and a size. This is intentionally heuristic because the three
    # sites use different HTML structures.
    current = anchor
    best = None
    for _ in range(6):
        if current is None:
            break
        txt = clean(current.get_text(" ", strip=True))
        if 30 <= len(txt) <= 1800:
            if extract_price(txt) is not None and (
                extract_size(txt) is not None or extract_rooms(txt) is not None
            ):
                best = txt
                break
        current = current.parent
    return best

def is_listing_link(href: str) -> bool:
    p = urlparse(href)
    path = p.path.lower()
    if not p.scheme in ("http", "https"):
        return False
    if any(x in path for x in ("/kontakt", "/login", "/blog", "/om-os", "/privacy")):
        return False
    return any(x in path for x in (
        "lejebolig", "lejeboliger", "bolig", "property", "apartment", "rental"
    ))

def parse_source(name: str, url: str) -> list:
    html = fetch(url)
    soup = BeautifulSoup(html, "html.parser")
    results = []
    seen_urls = set()

    for a in soup.find_all("a", href=True):
        href = urljoin(url, a["href"])
        if href in seen_urls or not is_listing_link(href):
            continue

        card = candidate_card(a)
        if not card:
            continue

        title = clean(a.get_text(" ", strip=True)) or card[:120]
        if len(title) > 180:
            title = title[:177] + "..."

        listing = {
            "source": name,
            "url": href,
            "title": title,
            "text": card,
            "rent": extract_price(card),
            "size_m2": extract_size(card),
            "rooms": extract_rooms(card),
        }

        # Only accept entries that look sufficiently like actual listings.
        if listing["rent"] is None:
            continue

        seen_urls.add(href)
        results.append(listing)

    return results
