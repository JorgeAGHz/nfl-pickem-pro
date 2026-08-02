from app.models import Season

from app.constants import (
    SPORT_NFL,
    SPORT_NBA,
    SEASON_UPCOMING,
    SEASON_ACTIVE,
    SEASON_CLOSED
)


# =====================================================
# CREATE
# =====================================================

def can_create_season(
    sport,
    year
):
    """
    A season can be created when:

    - Sport is valid
    - Year is valid
    - Another season with the same
      sport/year does not exist
    """

    if sport not in (
        SPORT_NFL,
        SPORT_NBA
    ):
        return False

    if year < 2000:
        return False

    existing = Season.query.filter_by(
        sport=sport,
        year=year
    ).first()

    return existing is None


# =====================================================
# ACTIVATE
# =====================================================

def can_activate(
    season
):
    """
    Only UPCOMING seasons
    may become ACTIVE.

    Only one ACTIVE season
    per sport.
    """

    if season.status != SEASON_UPCOMING:
        return False

    active = Season.query.filter_by(
        sport=season.sport,
        status=SEASON_ACTIVE
    ).first()

    return active is None


# =====================================================
# CLOSE
# =====================================================

def can_close(
    season
):
    """
    Only ACTIVE seasons
    may be closed.

    Additional validations
    (games, weeks, etc.)
    will be delegated later
    to Competition.
    """

    return (
        season.status ==
        SEASON_ACTIVE
    )


# =====================================================
# REOPEN
# =====================================================

def can_reopen(
    season
):
    """
    Only CLOSED seasons
    may reopen.
    """

    return (
        season.status ==
        SEASON_CLOSED
    )


# =====================================================
# ADVANCE WEEK
# =====================================================

def can_advance_week(
    season
):
    """
    Week progression
    is only allowed while
    ACTIVE.
    """

    if season.status != SEASON_ACTIVE:
        return False

    if season.current_week is None:
        return False

    return True


# =====================================================
# IMPORT GAMES
# =====================================================

def can_import_games(
    season
):
    """
    Games may be imported
    while the season is not
    closed.
    """

    return (
        season.status !=
        SEASON_CLOSED
    )


# =====================================================
# CREATE LEAGUE
# =====================================================

def can_create_league(
    season
):
    """
    Leagues can only be
    created in ACTIVE or
    UPCOMING seasons.
    """

    return season.status in (

        SEASON_ACTIVE,

        SEASON_UPCOMING

    )


# =====================================================
# WEEK VALIDATION
# =====================================================

def validate_week_number(
    week
):
    """
    Generic validation.

    Sport-specific limits
    will be handled later
    using SPORT_CONFIG.
    """

    if week is None:
        return False

    if week < 1:
        return False

    return True