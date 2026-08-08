import os
import requests

TELEGRAM_API = "https://api.telegram.org"

def send_telegram(text: str) -> None:
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    response = requests.post(
        f"{TELEGRAM_API}/bot{token}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text,
            "disable_web_page_preview": False,
        },
        timeout=20,
    )
    response.raise_for_status()

def send_test_message() -> None:
    send_telegram(
        "🏠 Copenhagen Apartment Hunter\n\n"
        "Telegram connection works. The scraper is ready to run."
    )
