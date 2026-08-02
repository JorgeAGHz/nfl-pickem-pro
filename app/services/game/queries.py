from app.models import Game

from app.constants import (
    GAME_STATUS_SCHEDULED,
    GAME_STATUS_IN_PROGRESS,
    GAME_STATUS_FINAL
)


# =====================================================
# SINGLE GAME
# =====================================================

def get_game(
    game_id
):
    """
    Returns a Game or None.
    """

    return Game.query.get(
        game_id
    )


# =====================================================
# API ID
# =====================================================

def get_game_by_api_id(
    season_id,
    api_id
):
    """
    Returns a Game using the
    provider identifier.
    """

    return Game.query.filter_by(

        season_id=season_id,

        api_id=api_id

    ).first()


# =====================================================
# WEEK
# =====================================================

def get_games_by_week(
    season_id,
    week
):
    """
    Returns every game
    for one week.
    """

    return (

        Game.query.filter_by(

            season_id=season_id,

            week=week

        )

        .order_by(
            Game.game_date
        )

        .all()

    )


# =====================================================
# SEASON
# =====================================================

def get_games_by_season(
    season_id
):
    """
    Returns every game
    of a season.
    """

    return (

        Game.query.filter_by(

            season_id=season_id

        )

        .order_by(

            Game.week,

            Game.game_date

        )

        .all()

    )


# =====================================================
# DATE RANGE
# =====================================================

def get_games_between_dates(
    start_date,
    end_date
):

    return (

        Game.query.filter(

            Game.game_date >= start_date,

            Game.game_date <= end_date

        )

        .order_by(

            Game.game_date

        )

        .all()

    )


# =====================================================
# LIVE
# =====================================================

def get_live_games():

    return (

        Game.query.filter_by(

            status=GAME_IN_PROGRESS

        )

        .order_by(

            Game.game_date

        )

        .all()

    )


# =====================================================
# FINAL
# =====================================================

def get_final_games():

    return (

        Game.query.filter_by(

            status=GAME_FINAL

        )

        .order_by(

            Game.game_date

        )

        .all()

    )