import os, requests
from models import Listing
from scoring import score

def send_telegram(listing):
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
    if not token or not chat_id:
        raise RuntimeError("Missing Telegram GitHub secrets.")
    price = f"{listing.price:,}".replace(",", ".") if listing.price else "N/A"
    size = f"{listing.size_m2:g} m²" if listing.size_m2 else "N/A"
    rooms = f"{listing.rooms:g}" if listing.rooms else "N/A"
    message = (f"🏠 NEW APARTMENT — {score(listing)}/100\n\n"
               f"📍 {listing.location or listing.title}\n"
               f"💰 {price} DKK/month\n📐 {size}\n🛏 {rooms} rooms\n"
               f"📅 {listing.available_from or 'Not specified'}\n🏢 {listing.source}\n\n"
               f"🔗 {listing.url}")
    r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                      json={"chat_id": chat_id, "text": message}, timeout=20)
    r.raise_for_status()
