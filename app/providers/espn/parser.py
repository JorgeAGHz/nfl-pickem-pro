from datetime import datetime

from .models import ParsedGame


class ESPNParser:
    """
    Converts ESPN JSON into ParsedGame
    objects.
    """

    # =====================================================
    # SCHEDULE
    # =====================================================

    def parse_schedule(
        self,
        payload: dict
    ) -> list[ParsedGame]:

        games: list[ParsedGame] = []

        for event in payload.get(
            "events",
            []
        ):

            competition = event["competitions"][0]

            competitors = competition["competitors"]

            home = next(
                c
                for c in competitors
                if c["homeAway"] == "home"
            )

            away = next(
                c
                for c in competitors
                if c["homeAway"] == "away"
            )

            games.append(

                ParsedGame(

                    api_id=event["id"],

                    season_type="REGULAR",

                    week=payload["week"]["number"],

                    game_date=datetime.fromisoformat(
                        event["date"].replace(
                            "Z",
                            "+00:00"
                        )
                    ),

                    home_team=home["team"]["displayName"],

                    away_team=away["team"]["displayName"],

                    home_abbr=home["team"]["abbreviation"],

                    away_abbr=away["team"]["abbreviation"],

                    home_logo=home["team"].get("logo"),

                    away_logo=away["team"].get("logo"),

                    home_score=(
                        int(home["score"])
                        if home["score"]
                        else None
                    ),

                    away_score=(
                        int(away["score"])
                        if away["score"]
                        else None
                    ),

                    spread=None,

                    status=event["status"]["type"]["description"],

                    clock=competition.get(
                        "status",
                        {}
                    ).get(
                        "displayClock"
                    ),

                    period=competition.get(
                        "status",
                        {}
                    ).get(
                        "period"
                    )

                )

            )

        return games