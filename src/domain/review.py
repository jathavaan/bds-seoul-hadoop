from dataclasses import dataclass
from datetime import datetime


@dataclass
class Review:
    id: int
    datePosted: datetime
    isRecommended: bool
    hoursPlayed: float

    def __post_init__(self):
        if isinstance(self.datePosted, str):
            self.datePosted = datetime.strptime(self.datePosted, "%Y-%m-%d")
