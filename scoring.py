from config import AREAS,BUDGET_MAX
def text(x): return f"{x.title} {x.location} {x.description}".lower()
def area_match(x): return any(a in text(x) for a in AREAS)
def matches(x):
    if x.price is not None and x.price>BUDGET_MAX:return False
    if x.rooms is not None and x.rooms<1:return False
    if x.location and not area_match(x):return False
    return not any(w in text(x) for w in ["værelse til leje","room for rent","shared room","delebolig","roommate"])
def score(x):
    s=45
    if x.price is not None:s+=25 if x.price<=11000 else 18 if x.price<=12000 else 10 if x.price<=13000 else 0
    if x.size_m2 is not None:s+=15 if x.size_m2>=70 else 10 if x.size_m2>=55 else 5 if x.size_m2>=45 else 0
    if x.rooms is not None:s+=10 if x.rooms>=3 else 8 if x.rooms>=2 else 0
    if area_match(x):s+=5
    return min(s,100)
