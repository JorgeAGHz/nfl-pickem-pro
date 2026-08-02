from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class ParsedGame:
    """
    Internal representation of a game
    coming from an external provider.

    This class is NOT a SQLAlchemy model.
    It only transports normalized data.
    """

    api_id: str

    season_type: str

    week: int

    game_date: datetime

    home_team: str
    away_team: str

    home_abbr: str
    away_abbr: str

    home_logo: str | None
    away_logo: str | None

    home_score: int | None
    away_score: int | None

    spread: float | None

    status: str | None

    clock: str | None

    period: int | None