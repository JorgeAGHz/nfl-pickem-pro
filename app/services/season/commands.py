from app.providers.espn.schedule import (
    ESPNScheduleService
)

from app.services.game.commands import (
    import_schedule
)

from datetime import datetime

from app.extensions import db

from app.models import Season

from app.constants import (
    SEASON_UPCOMING,
    SEASON_ACTIVE,
    SEASON_CLOSED
)

from .validators import (
    can_create_season,
    can_activate,
    can_close,
    can_reopen,
    can_advance_week,
    validate_week_number
)

from .queries import (
    get_season
)

from .exceptions import (
    SeasonAlreadyExistsError,
    InvalidSeasonTransitionError,
    InvalidWeekError,
    SeasonNotFoundError
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
    """

    if not can_create_season(
        sport,
        year
    ):
        raise SeasonAlreadyExistsError()

    season = Season(

        sport=sport,

        year=year,

        status=SEASON_UPCOMING,

        current_week=None

    )

    db.session.add(
        season
    )

    db.session.commit()

    return season


# =====================================================
# UPDATE
# =====================================================

def update_season(

    season_id,

    year=None

):
    """
    Updates editable
    season fields.
    """

    season = get_season(
        season_id
    )

    if season is None:
        raise SeasonNotFoundError()

    if year is not None:
        season.year = year

    season.updated_at = datetime.utcnow()

    db.session.commit()

    return season


# =====================================================
# ACTIVATE
# =====================================================

def activate_season(
    season_id
):

    season = get_season(
        season_id
    )

    if season is None:
        raise SeasonNotFoundError()

    if not can_activate(
        season
    ):
        raise InvalidSeasonTransitionError()

    season.status = SEASON_ACTIVE
    season.current_week = 1

    db.session.commit()

    provider = ESPNScheduleService()

    import_schedule(
        season,
        provider
    )

    return season


# =====================================================
# CLOSE
# =====================================================

def close_season(
    season_id
):

    season = get_season(
        season_id
    )

    if season is None:
        raise SeasonNotFoundError()

    if not can_close(
        season
    ):
        raise InvalidSeasonTransitionError()

    season.status = SEASON_CLOSED

    db.session.commit()

    return season


# =====================================================
# REOPEN
# =====================================================

def reopen_season(
    season_id
):

    season = get_season(
        season_id
    )

    if season is None:
        raise SeasonNotFoundError()

    if not can_reopen(
        season
    ):
        raise InvalidSeasonTransitionError()

    season.status = SEASON_ACTIVE

    db.session.commit()

    return season


# =====================================================
# ADVANCE WEEK
# =====================================================

def advance_week(
    season_id
):

    season = get_season(
        season_id
    )

    if season is None:
        raise SeasonNotFoundError()

    if not can_advance_week(
        season
    ):
        raise InvalidSeasonTransitionError()

    season.current_week += 1

    db.session.commit()

    return season


# =====================================================
# SET WEEK
# =====================================================

def set_current_week(
    season_id,
    week
):
    """
    Internal use only.

    Public UI will never
    expose this action.
    """

    season = get_season(
        season_id
    )

    if season is None:
        raise SeasonNotFoundError()

    if not validate_week_number(
        week
    ):
        raise InvalidWeekError()

    season.current_week = week

    db.session.commit()

    return season