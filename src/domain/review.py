from dataclasses import dataclass
from datetime import datetime


@dataclass
class Review:
    game_id: int
    datePosted: datetime
    isRecommended: bool
    hoursPlayed: float
    user_id: int

    def __post_init__(self):
        if isinstance(self.datePosted, str):
            self.datePosted = datetime.strptime(self.datePosted, "%Y-%m-%d")

    def __repr__(self):
        return f"{self.game_id},{self.datePosted},{1 if self.isRecommended else 0},{self.hoursPlayed},{self.user_id}"
