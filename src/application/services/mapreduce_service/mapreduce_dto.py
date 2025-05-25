from dataclasses import dataclass


@dataclass
class MapreduceDto:
    game_id: int
    correlation_id: str
    recommendations: dict[str, tuple[float, float]]

    def to_dict(self) -> dict[str, int | str | dict[str, tuple[float, float]]]:
        return {
            "game_id": self.game_id,
            "correlation_id": self.correlation_id,
            "recommendations": self.recommendations
        }
