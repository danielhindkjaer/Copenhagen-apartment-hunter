# Copenhagen Apartment Hunter 🏠

A personal-use Python/GitHub Actions project that checks selected public Copenhagen rental pages, filters listings against your criteria, remembers listings it has already seen, and sends matching new listings to Telegram.

## Current target

- Budget: max 13,000 DKK/month
- Move-in: November–December 2026
- Couple
- Student-friendly listings allowed
- Areas: Nørrebro, Østerbro, Frederiksberg, Valby, Sydhavn, Vesterbro, Nordvest, Amager, Nordhavn and nearby Copenhagen districts
- No minimum size
- 1+ rooms accepted, with 2+ rooms scored more highly

## Important

This is an intentionally conservative starter version. Websites change their HTML and some sites use anti-bot systems or terms that restrict automated access. The project only checks public pages and uses a low request rate. If a source blocks requests or prohibits automated access, disable that source and use its official alert/agent service instead.

## Setup

1. Create a GitHub repository and upload the files.
2. Go to:
   `Settings → Secrets and variables → Actions`
3. Add:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
4. Make sure Actions are enabled.
5. Go to `Actions → Copenhagen Apartment Hunter → Run workflow`.
6. Check Telegram.

The scheduled workflow then runs every five minutes.

## Do not put your Telegram token in the repository.

## Expanding sources

Add a public source to `SOURCES` in `config.py`, then create a dedicated parser in `scrapers.py` if its HTML structure is different.

The first version includes:
- BoligPortal public Copenhagen search
- Heimstaden Copenhagen
- Balder rental listings

The next sensible integrations are CEJ, Kereby, City Apartment and other property managers with public listing/alert pages.

## Why the state file exists

GitHub-hosted runners are ephemeral. `data/seen.json` records listing IDs that have already been seen. The workflow commits changes back to the repository so the next run knows what it has already notified you about.

## Testing locally

```bash
pip install -r requirements.txt
export TELEGRAM_BOT_TOKEN="..."
export TELEGRAM_CHAT_ID="..."
python main.py
```

On Windows PowerShell:

```powershell
$env:TELEGRAM_BOT_TOKEN="..."
$env:TELEGRAM_CHAT_ID="..."
python main.py
```
