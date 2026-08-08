from scrapers import scrape_all
from scoring import matches
from storage import load_seen, save_seen
from notify import send_telegram

def main():
    seen = load_seen()
    new_seen = set(seen)
    sent = 0
    for listing in scrape_all():
        if listing.key in seen: continue
        new_seen.add(listing.key)
        if matches(listing):
            try:
                send_telegram(listing); sent += 1
            except Exception as e:
                print(f"[WARN] Telegram failed: {e}")
    save_seen(new_seen)
    print(f"Sent {sent} new matches.")

if __name__ == "__main__":
    main()
