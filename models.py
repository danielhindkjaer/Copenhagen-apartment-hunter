from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Listing:
    source: str
    url: str
    title: str
    text: str
    rent: Optional[int] = None
    size_m2: Optional[float] = None
    rooms: Optional[float] = None
    area: Optional[str] = None
    available: Optional[str] = None
    published: Optional[str] = None
    score: int = 0
    score_label: str = ""
    reasons: list[str] = None

    def to_dict(self):
        d = asdict(self)
        d["reasons"] = self.reasons or []
        return d
