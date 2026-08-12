from config import TARGET_AREAS,EXCLUDED_LOCATIONS,BUDGET_MAX,MIN_SIZE_M2,MIN_ROOMS
def text(x): return f"{x.title} {x.location} {x.description}".lower()
def matches(x):
    if x.price is None or x.size_m2 is None or x.rooms is None: return False
    if not (0 < x.price <= BUDGET_MAX and x.size_m2 >= MIN_SIZE_M2 and x.rooms >= MIN_ROOMS): return False
    t=text(x)
    if any(c in t for c in EXCLUDED_LOCATIONS): return False
    if not any(a in t for a in TARGET_AREAS): return False
    return not any(w in t for w in ["værelse til leje","room for rent","shared room","delebolig","roommate","kollegieværelse","student room"])
def score(x):
    s=50
    s+=20 if x.price<=11000 else 12 if x.price<=12000 else 5
    s+=15 if x.size_m2>=70 else 10 if x.size_m2>=55 else 5 if x.size_m2>=45 else 0
    s+=10 if x.rooms>=3 else 7 if x.rooms>=2 else 0
    return min(s,100)
