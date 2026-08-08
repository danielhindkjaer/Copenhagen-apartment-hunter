import hashlib
import re
from datetime import datetime, timezone

from config import SOURCES
from models import Listing
from scoring import matches, score_listing
from scrapers import parse_source
from storage import load_seen, save_seen
from notify import send_telegram

def stable_id(listing: Listing) -> str:
    raw = f"{listing.source}|{listing.url}|{listing.rent}|{listing.size_m2}|{listing.rooms}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def format_money(value):
    return f"{value:,.0f}".replace(",", ".") if value is not None else "N/A"

def format_listing(l: Listing) -> str:
    reasons = ", ".join(l.reasons or [])
    return (
        f"🏠 NEW APARTMENT — {l.score_label}\n\n"
        f"📍 {l.area or 'Copenhagen area'}\n"
        f"💰 {format_money(l.rent)} DKK/month\n"
        f"📐 {l.size_m2:g} m²\n"
        f"🛏 {l.rooms:g} rooms\n"
        f"🏢 Source: {l.source}\n"
        f"⭐ Match: {l.score}/100 ({reasons})\n\n"
        f"🔗 {l.url}"
    )

def main():
    seen = load_seen()
    new_count = 0
    matched_count = 0

    for source in SOURCES:
        try:
            raw_listings = parse_source(source["name"], source["url"])
            print(f"{source['name']}: found {len(raw_listings)} candidates")
        except Exception as exc:
            print(f"ERROR {source['name']}: {exc}")
            continue

        for raw in raw_listings:
            listing = score_listing(Listing(**raw))
            key = stable_id(listing)

            if key in seen:
                continue

            seen[key] = {
                "first_seen": datetime.now(timezone.utc).isoformat(),
                "url": listing.url,
                "source": listing.source,
            }
            new_count += 1

            if matches(listing):
                matched_count += 1
                try:
                    send_telegram(format_listing(listing))
                except Exception as exc:
                    print(f"Telegram error: {exc}")

    save_seen(seen)
    print(f"New listings: {new_count}; matching: {matched_count}")

if __name__ == "__main__":
    main()
