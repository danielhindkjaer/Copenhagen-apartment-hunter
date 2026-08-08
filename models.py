from dataclasses import dataclass
from typing import Optional

@dataclass
class Listing:
    title: str
    url: str
    source: str
    price: Optional[int] = None
    size_m2: Optional[float] = None
    rooms: Optional[float] = None
    location: str = ""
    available_from: str = ""
    description: str = ""

    @property
    def key(self):
        return self.url.strip()
