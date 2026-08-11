from scrapers import scrape_all
from scoring import matches
from storage import load_seen,save_seen
from notify import send_telegram
def main():
    seen=load_seen(); listings=scrape_all(); new_seen=set(seen); new_count=sent=0
    for x in listings:
        if x.key in seen:continue
        new_count+=1;new_seen.add(x.key)
        if not matches(x):continue
        try:send_telegram(x);sent+=1;print(f"[SENT] {x.source}: {x.title}")
        except Exception as e:print(f"[WARN] Telegram failed: {e}")
    save_seen(new_seen);print(f"[DONE] Checked {len(listings)} unique listings; {new_count} new; {sent} alerts.")
if __name__=="__main__":main()
