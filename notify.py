import os,requests
from scoring import score
def send_telegram(x):
    token=os.environ.get("TELEGRAM_BOT_TOKEN",""); chat_id=os.environ.get("TELEGRAM_CHAT_ID","")
    if not token or not chat_id: raise RuntimeError("Missing Telegram secrets.")
    msg=(f"🏠 NEW APARTMENT — {score(x)}/100\n\n📍 {x.location}\n💰 {x.price:,} DKK/month\n📐 {x.size_m2:g} m²\n🛏 {x.rooms:g} rooms\n📅 {x.available_from or 'Not specified'}\n🏢 {x.source}\n\n🔗 {x.url}")
    r=requests.post(f"https://api.telegram.org/bot{token}/sendMessage",json={"chat_id":chat_id,"text":msg},timeout=20); r.raise_for_status()
