from models import Listing
from config import BUDGET_MAX, AREAS

def matches(listing):
    if listing.price is not None and listing.price > BUDGET_MAX: return False
    text = f"{listing.title} {listing.location} {listing.description}".lower()
    return not listing.location or any(a in text for a in AREAS)

def score(listing):
    value = 50
    if listing.price and listing.price <= 12000: value += 20
    elif listing.price and listing.price <= 13000: value += 10
    if listing.size_m2 and listing.size_m2 >= 60: value += 15
    elif listing.size_m2 and listing.size_m2 >= 50: value += 10
    if listing.rooms and listing.rooms >= 2: value += 10
    return min(value, 100)
