# Copenhagen Apartment Hunter

GitHub Actions + Python monitor for Copenhagen rentals.

Current filters: up to 13,000 DKK/month; Copenhagen areas including Nørrebro, Østerbro, Frederiksberg, Valby, Sydhavn, Vesterbro, Nordvest, Amager, Nordhavn, Islands Brygge and Ørestad; target move-in November/December 2026.

## Setup
Add GitHub Actions secrets:
- TELEGRAM_BOT_TOKEN
- TELEGRAM_CHAT_ID

Then go to Actions → Copenhagen Apartment Hunter → Run workflow.

The workflow runs every 10 minutes. Public-page scraping only; it does not bypass login, CAPTCHA, paywalls or anti-bot controls.
