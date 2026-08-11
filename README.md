# Copenhagen Apartment Hunter — Kereby + Grønttorvet

Search: max 13,000 DKK/month, no minimum size, whole apartment/couple focus, requested Copenhagen areas, move-in Nov/Dec 2026.

Sources: BoligPortal, Heimstaden, Balder, Lejebolig.dk, Lejeboligportal.dk, Bolig.dk, City Apartment, Taurus, Newsec, CEJ, Juli Living, Findbolig, Housing Denmark, AkutBolig, Kereby and Grønttorvet.

IMPORTANT: Keep the existing data/seen.json from your CURRENT working GitHub repository. Do not replace it with this ZIP's empty data/seen.json, or the bot may treat existing listings as new.

NEW logic: a URL already in seen.json never triggers again. A new URL is filtered and, if it matches, sent to Telegram; then it is stored.

Some sites are JavaScript-heavy, so the generic scraper may return zero candidates even when listings exist. This version adds Kereby and Grønttorvet to the source list; dedicated adapters can be added later if needed.

Secrets: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID.
