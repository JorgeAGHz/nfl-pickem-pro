from datetime import datetime, timezone

from app.extensions import db

from app.models import Game

from app.constants import (
    SPORT_NFL,
    SPORT_NBA,

    SEASON_TYPE_REGULAR,
    SEASON_TYPE_PLAYOFF,

    GAME_STATUS_SCHEDULED,
    GAME_STATUS_IN_PROGRESS,
    GAME_STATUS_FINAL,
    NFL_FINAL_WEEK
)

from app.services.espn_client import (
    get_nfl_scoreboard
)


# =====================================================
# HELPERS
# =====================================================

def parse_espn_datetime(value):

    if not value:
        return None

    return datetime.fromisoformat(
        value.replace("Z", "+00:00")
    ).astimezone(timezone.utc)


def normalize_status(raw_status):

    if not raw_status:
        return GAME_STATUS_SCHEDULED

    value = raw_status.lower()

    if "final" in value:
        return GAME_STATUS_FINAL

    if (
        "progress" in value
        or
        "halftime" in value
        or
        "live" in value
    ):
        return GAME_STATUS_IN_PROGRESS

    return GAME_STATUS_SCHEDULED


def get_season_type(week):

    if week <= 18:
        return SEASON_TYPE_REGULAR

    return SEASON_TYPE_PLAYOFF


# =====================================================
# UPSERT GAME
# =====================================================

def upsert_game(
    season,
    game_data
):

    game = Game.query.filter_by(
        season_id=season.id,
        api_id=game_data["api_id"]
    ).first()

    if not game:

        game = Game(
            season_id=season.id,
            api_id=game_data["api_id"]
        )

        db.session.add(game)

    game.home_team = game_data["home_team"]
    game.away_team = game_data["away_team"]

    game.home_abbr = game_data["home_abbr"]
    game.away_abbr = game_data["away_abbr"]

    game.home_logo = game_data["home_logo"]
    game.away_logo = game_data["away_logo"]

    game.game_date = game_data["game_date"]

    game.week = game_data["week"]

    game.season_type = game_data["season_type"]

    game.spread = game_data["spread"]

    game.home_odds = game_data["home_odds"]
    game.away_odds = game_data["away_odds"]

    game.status = game_data["status"]

    game.clock = game_data["clock"]
    game.period = game_data["period"]

    game.home_score = game_data["home_score"]
    game.away_score = game_data["away_score"]

    return game


# =====================================================
# IMPORT NFL SEASON
# =====================================================

def import_nfl_season(
    season
):

    if season.sport != SPORT_NFL:

        raise ValueError(
            "Season is not NFL."
        )

    imported = 0

    for week in range(
        1,
        NFL_FINAL_WEEK + 1
    ):

        data = get_nfl_scoreboard(
            season.year,
            week
        )

        for event in data.get(
            "events",
            []
        ):

            parsed = parse_nfl_event(
                event,
                week
            )

            upsert_game(
                season,
                parsed
            )

            imported += 1

    db.session.commit()

    return imported


# =====================================================
# PARSE NFL EVENT
# =====================================================

def parse_nfl_event(
    event,
    week
):

    comp = event["competitions"][0]

    competitors = comp[
        "competitors"
    ]

    home = next(
        x for x in competitors
        if x["homeAway"] == "home"
    )

    away = next(
        x for x in competitors
        if x["homeAway"] == "away"
    )

    odds = None

    if comp.get("odds"):
        odds = comp["odds"][0]

    return {

        "api_id":
            event["id"],

        "home_team":
            home["team"]["displayName"],

        "away_team":
            away["team"]["displayName"],

        "home_abbr":
            home["team"]["abbreviation"],

        "away_abbr":
            away["team"]["abbreviation"],

        "home_logo":
            home["team"]
            .get("logos", [{}])[0]
            .get("href"),

        "away_logo":
            away["team"]
            .get("logos", [{}])[0]
            .get("href"),

        "game_date":
            parse_espn_datetime(
                event["date"]
            ),

        "week":
            week,

        "season_type":
            get_season_type(
                week
            ),

        "spread":
            (
                odds.get("spread")
                if odds
                else None
            ),

        "home_odds":
            (
                odds.get(
                    "homeMoneyLine"
                )
                if odds
                else None
            ),

        "away_odds":
            (
                odds.get(
                    "awayMoneyLine"
                )
                if odds
                else None
            ),

        "status":
            normalize_status(
                comp["status"]["type"]
                .get(
                    "description"
                )
            ),

        "clock":
            comp["status"]
            .get(
                "displayClock"
            ),

        "period":
            comp["status"]
            .get(
                "period"
            ),

        "home_score":
            int(
                home.get(
                    "score",
                    0
                )
            ),

        "away_score":
            int(
                away.get(
                    "score",
                    0
                )
            )
    }