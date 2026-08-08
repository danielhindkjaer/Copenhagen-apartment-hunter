import re, requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from models import Listing
from config import REQUEST_TIMEOUT, MAX_LISTINGS_PER_SOURCE

HEADERS = {"User-Agent": "CopenhagenApartmentHunter/1.0"}
SOURCES = {
    "BoligPortal": "https://www.boligportal.dk/lejeboliger/koebenhavn/",
    "Heimstaden": "https://www.heimstaden.dk/lejebolig/",
    "Balder": "https://www.balder.dk/boligportal",
}

def _size(t):
    m = re.search(r"(\d+(?:[\.,]\d+)?)\s*m²", t, re.I)
    return float(m.group(1).replace(",", ".")) if m else None

def _rooms(t):
    m = re.search(r"(\d+(?:[\.,]\d+)?)\s*(?:værelser|rooms?|rum)", t, re.I)
    return float(m.group(1).replace(",", ".")) if m else None

def _price(t):
    m = re.search(r"(\d[\d\.\s]*)\s*(?:kr|dkk)", t, re.I)
    if not m: return None
    try: return int(m.group(1).replace(" ","").replace(".",""))
    except ValueError: return None

def scrape_source(source, url):
    r = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    out, urls = [], set()
    for a in soup.find_all("a", href=True):
        href = urljoin(url, a["href"])
        title = " ".join(a.get_text(" ", strip=True).split())
        if not title or href in urls: continue
        parent = a.parent
        blob = title + (" " + " ".join(parent.get_text(" ", strip=True).split()) if parent else "")
        if not re.search(r"\b(kr|dkk|m²|værelser|rooms|lejebolig|bolig|apartment|rent)\b", blob, re.I):
            continue
        urls.add(href)
        out.append(Listing(title=title[:200], url=href, source=source,
                           price=_price(blob), size_m2=_size(blob), rooms=_rooms(blob),
                           location=blob[:300], description=blob[:1000]))
        if len(out) >= MAX_LISTINGS_PER_SOURCE: break
    return out

def scrape_all():
    out = []
    for source, url in SOURCES.items():
        try: out.extend(scrape_source(source, url))
        except Exception as e: print(f"[WARN] {source}: {e}")
    return out
