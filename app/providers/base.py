from typing import Protocol

from app.models import Season


class SportsProvider(Protocol):
    """
    Contract that every sports
    provider must implement.

    Providers are responsible for
    communicating with external APIs.

    They NEVER access the database.
    """

    # ---------------------------------
    # Seasons
    # ---------------------------------

    def get_current_week(
        self,
        season: Season
    ) -> int:
        ...

    # ---------------------------------
    # Schedule
    # ---------------------------------

    def get_schedule(
        self,
        season: Season
    ) -> list:
        ...

    # ---------------------------------
    # Scores
    # ---------------------------------

    def update_scores(
        self,
        season: Season
    ) -> list:
        ...

    # ---------------------------------
    # Single Game
    # ---------------------------------

    def get_game(
        self,
        external_game_id: str
    ) -> dict:
        ...