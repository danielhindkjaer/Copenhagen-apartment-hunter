from config import CONFIG
from models import Listing

def area_match(text: str) -> str | None:
    lower = text.lower()
    for area in CONFIG.areas:
        if area.lower() in lower:
            return area
    return None

def score_listing(listing: Listing) -> Listing:
    text = f"{listing.title} {listing.text}".lower()
    reasons = []
    score = 0

    if listing.rent is not None:
        if listing.rent <= CONFIG.max_rent:
            score += 35
            reasons.append("within budget")
        else:
            return listing

    if listing.rooms is not None:
        if listing.rooms >= 2:
            score += 20
            reasons.append("2+ rooms")
        elif listing.rooms >= 1:
            score += 10
            reasons.append("1 room")

    if listing.size_m2 is not None:
        if listing.size_m2 >= 55:
            score += 20
            reasons.append("55+ m²")
        elif listing.size_m2 >= 40:
            score += 10
            reasons.append("40+ m²")

    listing.area = listing.area or area_match(text)
    if listing.area:
        score += 20
        reasons.append(listing.area)

    if any(k in text for k in CONFIG.positive_keywords):
        score += 5

    listing.score = min(score, 100)
    if listing.score >= 80:
        listing.score_label = "★★★★★"
    elif listing.score >= 65:
        listing.score_label = "★★★★"
    elif listing.score >= 50:
        listing.score_label = "★★★"
    elif listing.score >= 35:
        listing.score_label = "★★"
    else:
        listing.score_label = "★"

    listing.reasons = reasons
    return listing

def matches(listing: Listing) -> bool:
    text = f"{listing.title} {listing.text}".lower()

    if any(k.lower() in text for k in CONFIG.reject_keywords):
        return False

    # If a source provides price, enforce the budget.
    if listing.rent is not None and not (
        CONFIG.min_rent <= listing.rent <= CONFIG.max_rent
    ):
        return False

    # We do not reject missing room/size information: parsers can be imperfect.
    if listing.rooms is not None and listing.rooms < CONFIG.min_rooms:
        return False

    # Prefer the target area, but do not require it when the source has poor
    # address extraction. This avoids silently losing good listings.
    if listing.area is None and not area_match(text):
        return False

    # Student-only homes are allowed because the user is a student. Couple
    # eligibility should be checked on the individual listing before applying.
    return True
