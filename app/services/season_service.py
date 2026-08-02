from app.extensions import db

from app.models import Season

from app.constants import (
    SEASON_UPCOMING,
    SEASON_ACTIVE,
    SEASON_CLOSED,
    SPORT_NFL,
    NFL_FINAL_WEEK
)


# =====================================================
# CREATE
# =====================================================

def create_season(
    sport,
    year
):
    """
    Creates a new season.

    NFL starts on week 1.
    NBA uses current_week=None.
    """

    current_week = None

    if sport == SPORT_NFL:
        current_week = 1

    season = Season(
        sport=sport,
        year=year,
        status=SEASON_UPCOMING,
        current_week=current_week
    )

    db.session.add(season)
    db.session.commit()

    return season


# =====================================================
# ACTIVATE
# =====================================================

def activate_season(season):
    """
    Only one ACTIVE season
    per sport.
    """

    active = Season.query.filter(
        Season.sport == season.sport,
        Season.status == SEASON_ACTIVE,
        Season.id != season.id
    ).first()

    if active:
        raise ValueError(
            f"There is already an active "
            f"{season.sport} season."
        )

    season.status = SEASON_ACTIVE

    db.session.commit()

    return season


# =====================================================
# CLOSE
# =====================================================

def close_season(season):

    season.status = SEASON_CLOSED

    db.session.commit()

    return season


# =====================================================
# ADVANCE WEEK
# =====================================================

def advance_week(season):
    """
    NFL:
        1 -> 22

    NBA:
        No-op
    """

    if season.current_week is None:
        return season

    if season.current_week >= NFL_FINAL_WEEK:
        raise ValueError(
            "Season already reached final week."
        )

    season.current_week += 1

    db.session.commit()

    return season


# =====================================================
# HELPERS
# =====================================================

def get_active_season(sport):

    return Season.query.filter_by(
        sport=sport,
        status=SEASON_ACTIVE
    ).first()


def season_is_active(season):

    return season.status == SEASON_ACTIVE


def season_is_closed(season):

    return season.status == SEASON_CLOSED


def season_is_upcoming(season):

    return season.status == SEASON_UPCOMING