from .client import ESPNClient
from .parser import ESPNParser


class ESPNScheduleService:
    """
    Coordinates schedule imports.

    Responsibilities:

    - Call ESPN

    - Parse JSON

    - Return ParsedGame objects

    No business rules.

    No SQLAlchemy.
    """

    def __init__(self):

        self.client = ESPNClient()

        self.parser = ESPNParser()

    # =====================================================
    # IMPORT
    # =====================================================

    def import_schedule(
        self,
        year: int,
        week: int,
        season_type: int = 2
    ):

        payload = self.client.get_nfl_schedule(

            year=year,

            week=week,

            season_type=season_type

        )

        return self.parser.parse_schedule(
            payload
        )