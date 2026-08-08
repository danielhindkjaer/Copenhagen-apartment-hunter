from dataclasses import dataclass, field

@dataclass(frozen=True)
class SearchConfig:
    max_rent: int = 13_000
    min_rent: int = 0
    min_rooms: float = 1
    min_size_m2: float = 0
    move_in_from: str = "2026-11-01"
    move_in_to: str = "2026-12-31"

    # User is a student, but is also looking as a couple.
    allow_student_only: bool = True
    require_couple_friendly: bool = False

    areas: tuple[str, ...] = (
        "Nørrebro",
        "København N",
        "Østerbro",
        "København Ø",
        "Frederiksberg",
        "Frederiksberg C",
        "Valby",
        "København SV",
        "Sydhavn",
        "København S",
        "Amager",
        "Nordhavn",
        "København NV",
        "Nordvest",
        "Vesterbro",
        "København V",
        "Islands Brygge",
        "Ørestad",
        "Amagerbro",
        "Amager Strand",
    )

    # Keywords that strongly suggest this is not a normal couple apartment.
    reject_keywords: tuple[str, ...] = (
        "room for rent",
        "værelse til leje",
        "roommate",
        "roomie",
        "kollegieværelse",
        "værelseslejemål",
        "parking",
        "garage",
        "kontor",
        "erhverv",
    )

    # Keywords that increase the score for a couple.
    positive_keywords: tuple[str, ...] = (
        "lejlighed",
        "apartment",
        "2 vær",
        "3 vær",
        "4 vær",
        "par",
        "couple",
        "stue",
        "soveværelse",
    )

CONFIG = SearchConfig()

# Public pages only. Do not add authenticated URLs or credentials here.
SOURCES = [
    {
        "name": "BoligPortal",
        "url": "https://www.boligportal.dk/lejeboliger/k%C3%B8benhavn/",
        "domains": ("boligportal.dk",),
    },
    {
        "name": "Heimstaden",
        "url": "https://www.heimstaden.dk/lejeboliger/koebenhavn/",
        "domains": ("heimstaden.dk",),
    },
    {
        "name": "Balder",
        "url": "https://www.balder.dk/lejeboliger",
        "domains": ("balder.dk",),
    },
]
