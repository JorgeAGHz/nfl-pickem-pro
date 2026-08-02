from .client import ESPNClient
from .parser import ESPNParser


class ESPNScoresService:
    """
    Coordinates score updates.

    Returns ParsedGame objects.
    """

    def __init__(self):

        self.client = ESPNClient()

        self.parser = ESPNParser()

    # =====================================================
    # UPDATE
    # =====================================================

    def update_scores(
        self
    ):

        payload = self.client.get_nfl_scoreboard()

        return self.parser.parse_schedule(
            payload
        )