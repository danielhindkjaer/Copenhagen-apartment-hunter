import os,requests
from scoring import score
def send_telegram(x):
    token=os.environ.get("TELEGRAM_BOT_TOKEN",""); chat_id=os.environ.get("TELEGRAM_CHAT_ID","")
    if not token or not chat_id: raise RuntimeError("Missing Telegram secrets.")
    p=f"{x.price:,}".replace(",",".") if x.price is not None else "N/A"
    z=f"{x.size_m2:g} m²" if x.size_m2 is not None else "N/A"
    r=f"{x.rooms:g}" if x.rooms is not None else "N/A"
    msg=f"🏠 NEW APARTMENT — {score(x)}/100\n\n📍 {x.location or x.title}\n💰 {p} DKK/month\n📐 {z}\n🛏 {r} rooms\n📅 {x.available_from or 'Not specified'}\n🏢 {x.source}\n\n🔗 {x.url}"
    q=requests.post(f"https://api.telegram.org/bot{token}/sendMessage",json={"chat_id":chat_id,"text":msg},timeout=20); q.raise_for_status()
