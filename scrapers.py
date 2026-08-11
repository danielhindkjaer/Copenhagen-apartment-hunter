import re,requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from config import REQUEST_TIMEOUT,MAX_LISTINGS_PER_SOURCE
from models import Listing
HEADERS={"User-Agent":"Mozilla/5.0 CopenhagenApartmentHunter/1.0"}
SOURCES={
"BoligPortal":"https://www.boligportal.dk/lejeboliger/koebenhavn/",
"Heimstaden":"https://www.heimstaden.dk/","Balder":"https://www.balder.dk/",
"Lejebolig.dk":"https://www.lejebolig.dk/lejeboliger/koebenhavn",
"Lejeboligportal.dk":"https://www.lejeboligportal.dk/","Bolig.dk":"https://www.bolig.dk/",
"City Apartment":"https://cityapartment.dk/","Taurus":"https://www.taurus.dk/",
"Newsec":"https://bolig.newsec.dk/","CEJ":"https://udlejning.cej.dk/",
"Juli Living":"https://juliliving.dk/","Findbolig":"https://findbolig.nu/",
"Housing Denmark":"https://housingdenmark.com/","AkutBolig":"https://www.akutbolig.dk/",
"Kereby":"https://kereby.dk/bolig/","Grønttorvet":"https://groenttorvet.dk/"}
def clean(t):return " ".join(t.replace("\xa0"," ").split())
def price(t):
    for p in [r"(\d[\d\.\s]*)\s*(?:kr\.?|dkk)",r"(?:rent|husleje)\s*[:\-]?\s*(\d[\d\.\s]*)"]:
        m=re.search(p,t,re.I)
        if m:
            try:return int(m.group(1).replace(" ","").replace(".","").replace(",",""))
            except:pass
    return None
def size(t):
    m=re.search(r"(\d+(?:[.,]\d+)?)\s*m²",t,re.I); return float(m.group(1).replace(",",".")) if m else None
def rooms(t):
    m=re.search(r"(\d+(?:[.,]\d+)?)\s*(?:værelser|vær\.?|rooms?|rum)",t,re.I); return float(m.group(1).replace(",",".")) if m else None
def availability(t):
    m=re.search(r"(?:overtagelsesdato|available from|move[- ]?in|indflytning)\s*[:\-]?\s*([0-9]{1,2}[./-][0-9]{1,2}[./-][0-9]{2,4})",t,re.I); return m.group(1) if m else ""
def scrape_source(source,start_url):
    q=requests.get(start_url,headers=HEADERS,timeout=REQUEST_TIMEOUT,allow_redirects=True);q.raise_for_status()
    soup=BeautifulSoup(q.text,"html.parser");out=[];seen=set()
    terms=["lejlighed","lejebolig","bolig","apartment","rental","rent","værelse","room","m²","kr","dkk"]
    for a in soup.find_all("a",href=True):
        href=urljoin(q.url,a["href"]);title=clean(a.get_text(" ",strip=True))
        if not title or href in seen:continue
        parent=clean(a.parent.get_text(" ",strip=True)) if a.parent else "";blob=clean(title+" "+parent)
        if not any(t in blob.lower() for t in terms):continue
        if any(t in title.lower() for t in ["log ind","login","kontakt","contact","opret bruger","sign up","privacy","cookie"]):continue
        seen.add(href);out.append(Listing(title[:200],href,source,price(blob),size(blob),rooms(blob),blob[:400],availability(blob),blob[:1500]))
        if len(out)>=MAX_LISTINGS_PER_SOURCE:break
    return out
def scrape_all():
    all_items=[]
    for source,url in SOURCES.items():
        try:
            items=scrape_source(source,url);print(f"[OK] {source}: {len(items)} candidates");all_items+=items
        except Exception as e:print(f"[WARN] {source}: {type(e).__name__}: {e}")
    unique={x.key:x for x in all_items};print(f"[SUMMARY] {len(all_items)} candidates -> {len(unique)} unique URLs");return list(unique.values())
