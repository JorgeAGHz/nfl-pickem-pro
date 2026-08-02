from __future__ import annotations

import requests

from requests import Response
from requests.exceptions import RequestException


BASE_URL = "https://site.api.espn.com/apis/site/v2/sports"


class ESPNClient:
    """
    Low-level HTTP client.

    Responsibilities:

    - Build URLs
    - Execute HTTP requests
    - Return JSON

    It NEVER knows about SQLAlchemy,
    Game models or business rules.
    """

    def __init__(
        self,
        timeout: int = 15
    ):

        self.timeout = timeout

    # =====================================================
    # INTERNAL
    # =====================================================

    def _get(
        self,
        endpoint: str,
        params: dict | None = None
    ) -> dict:

        url = f"{BASE_URL}/{endpoint}"

        try:

            response: Response = requests.get(

                url,

                params=params,

                timeout=self.timeout

            )

            response.raise_for_status()

            return response.json()

        except RequestException as exc:

            raise RuntimeError(

                f"ESPN request failed: {exc}"

            ) from exc

    # =====================================================
    # NFL SCHEDULE
    # =====================================================

    def get_nfl_schedule(
        self,
        year: int,
        week: int,
        season_type: int = 2
    ) -> dict:
        """
        season_type

        1 = Preseason
        2 = Regular Season
        3 = Postseason
        """

        return self._get(

            "football/nfl/scoreboard",

            params={

                "dates": year,

                "seasontype": season_type,

                "week": week

            }

        )

    # =====================================================
    # NFL SCOREBOARD
    # =====================================================

    def get_nfl_scoreboard(
        self
    ) -> dict:

        return self._get(

            "football/nfl/scoreboard"

        )