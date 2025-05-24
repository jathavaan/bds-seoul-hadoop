from dataclasses import dataclass
from datetime import datetime


@dataclass
class Review:
    game_id: int
    date_posted: datetime
    is_recommended: bool
    hours_played: float
    user_id: int
    is_last_review: bool
    correlation_id: str

    def __post_init__(self):
        if isinstance(self.date_posted, str):
            self.date_posted = datetime.strptime(self.date_posted, "%Y-%m-%d")

    def __repr__(self):
        """
        Do NOT change this unless more fields are being added to the Map Reduce job
        :return: Returns string on the format for Map Reduce job
        """
        return f"{self.game_id},{self.date_posted},{1 if self.is_recommended else 0},{self.hours_played},{self.user_id}"
