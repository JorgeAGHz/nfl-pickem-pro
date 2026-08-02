from app.extensions import db

from app.models import (
    Game,
    Season
)

from app.constants import (
    SPORT_NFL,
    SPORT_NBA,

    GAME_STATUS_FINAL,
    GAME_STATUS_IN_PROGRESS,
    GAME_STATUS_SCHEDULED
)

from app.services.espn_client import (
    get_nba_scoreboard,
    get_nfl_scoreboard_today
)

from app.services.espn_import_service import (
    normalize_status
)


# =====================================================
# PUBLIC
# =====================================================

def update_live_games():

    updated = 0

    updated += update_nfl_games()

    updated += update_nba_games()

    db.session.commit()

    return updated


# =====================================================
# NFL
# =====================================================

def update_nfl_games():

    data = get_nfl_scoreboard_today()

    return process_scoreboard(
        data
    )


# =====================================================
# NBA
# =====================================================

def update_nba_games():

    data = get_nba_scoreboard()

    return process_scoreboard(
        data
    )


# =====================================================
# SCOREBOARD
# =====================================================

def process_scoreboard(
    data
):

    updated = 0

    events = data.get(
        "events",
        []
    )

    for event in events:

        api_id = event["id"]

        game = Game.query.filter_by(
            api_id=api_id
        ).first()

        if not game:
            continue

        comp = event[
            "competitions"
        ][0]

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

        game.home_score = int(
            home.get(
                "score",
                0
            )
        )

        game.away_score = int(
            away.get(
                "score",
                0
            )
        )

        game.status = normalize_status(
            comp["status"]["type"]
            .get(
                "description"
            )
        )

        game.clock = comp[
            "status"
        ].get(
            "displayClock"
        )

        game.period = comp[
            "status"
        ].get(
            "period"
        )

        updated += 1

    return updated