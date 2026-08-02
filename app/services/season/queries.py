from app.models import Season

from app.constants import (
    SPORT_NFL,
    SPORT_NBA,
    SEASON_ACTIVE,
    SEASON_UPCOMING
)


# =====================================================
# SINGLE SEASON
# =====================================================

def get_season(
    season_id
):
    """
    Returns the season or None.
    """

    return Season.query.get(
        season_id
    )


# =====================================================
# ACTIVE
# =====================================================

def get_active_season(
    sport
):
    """
    Returns the active season
    for a sport.
    """

    return Season.query.filter_by(

        sport=sport,

        status=SEASON_ACTIVE

    ).first()


# =====================================================
# AVAILABLE
# =====================================================

def get_available_seasons():
    """
    Seasons that may receive
    new leagues.

    ACTIVE
    UPCOMING
    """

    return (

        Season.query.filter(

            Season.status.in_(

                (

                    SEASON_ACTIVE,

                    SEASON_UPCOMING

                )

            )

        )

        .order_by(

            Season.sport,

            Season.year.desc()

        )

        .all()

    )


# =====================================================
# UPCOMING
# =====================================================

def get_upcoming_seasons():
    """
    Returns every upcoming
    season.
    """

    return (

        Season.query.filter_by(

            status=SEASON_UPCOMING

        )

        .order_by(

            Season.sport,

            Season.year

        )

        .all()

    )


# =====================================================
# ALL
# =====================================================

def get_all_seasons():
    """
    Returns every season.
    """

    return (

        Season.query.order_by(

            Season.sport,

            Season.year.desc()

        )

        .all()

    )


# =====================================================
# SPORT
# =====================================================

def get_seasons_by_sport(
    sport
):
    """
    Returns all seasons
    for a sport.
    """

    if sport not in (

        SPORT_NFL,

        SPORT_NBA

    ):

        return []

    return (

        Season.query.filter_by(

            sport=sport

        )

        .order_by(

            Season.year.desc()

        )

        .all()

    )


# =====================================================
# EXISTS
# =====================================================

def season_exists(
    sport,
    year
):
    """
    True if the season
    already exists.
    """

    return (

        Season.query.filter_by(

            sport=sport,

            year=year

        ).first()

        is not None

    )