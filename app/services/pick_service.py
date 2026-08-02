from datetime import datetime
from zoneinfo import ZoneInfo

from app.extensions import db

from app.models import (
    Pick,
    Game
)

from app.constants import (
    VALID_SELECTIONS_BY_MODE,
    NFL_REGULAR_SEASON_END
)

MEXICO_TZ = ZoneInfo("America/Mexico_City")


# =====================================================
# GAME STATUS
# =====================================================

def game_started(game):
    """
    Returns True if kickoff/tipoff
    has already happened.
    """

    if not game.game_date:
        return False

    now = datetime.now(
        tz=game.game_date.tzinfo
    )

    return now >= game.game_date


# =====================================================
# PICK EDITING
# =====================================================

def can_edit_pick(game):

    return not game_started(game)


# =====================================================
# PICK VISIBILITY
# =====================================================

def can_view_pick(
    game,
    viewer_id,
    owner_id
):
    """
    Before game starts:

        Owner can see own pick

        Others cannot

    After game starts:

        Everyone can see
    """

    if game_started(game):
        return True

    return viewer_id == owner_id


# =====================================================
# VALIDATION
# =====================================================

def validate_selection(
    league,
    selection
):

    pick_mode = league.settings.pick_mode

    valid_options = VALID_SELECTIONS_BY_MODE.get(
        pick_mode
    )

    if not valid_options:

        raise ValueError(
            "Invalid league pick mode."
        )

    if selection not in valid_options:

        raise ValueError(
            f"Selection '{selection}' "
            f"is not allowed for "
            f"pick mode '{pick_mode}'."
        )


# =====================================================
# SAVE PICK
# =====================================================

def save_pick(
    user,
    league,
    game,
    selection
):
    """
    Creates or updates
    a single pick.
    """

    validate_selection(
        league,
        selection
    )

    if not can_edit_pick(game):

        raise ValueError(
            "Game already started."
        )

    # -------------------------------------
    # Safety check:
    # game must belong to league season
    # -------------------------------------

    if game.season_id != league.season_id:

        raise ValueError(
            "Game does not belong "
            "to league season."
        )

    # -------------------------------------
    # Playoff restriction
    # -------------------------------------

    if (
        not league.settings.include_playoffs
        and game.week
        and game.week > NFL_REGULAR_SEASON_END
    ):

        raise ValueError(
            "Playoff picks are disabled "
            "for this league."
        )

    pick = Pick.query.filter_by(
        user_id=user.id,
        league_id=league.id,
        game_id=game.id
    ).first()

    if not pick:

        pick = Pick(
            user_id=user.id,
            league_id=league.id,
            game_id=game.id,
            selection=selection
        )

        db.session.add(pick)

    else:

        pick.selection = selection

    db.session.commit()

    return pick


# =====================================================
# GET USER PICK
# =====================================================

def get_user_pick(
    user_id,
    league_id,
    game_id
):

    return Pick.query.filter_by(
        user_id=user_id,
        league_id=league_id,
        game_id=game_id
    ).first()


# =====================================================
# CURRENT WEEK GAMES
# =====================================================

def get_current_week_games(
    league
):
    """
    Returns only games that
    belong to the active
    competition window.
    """

    season = league.season

    # NFL

    if season.current_week is not None:

        if (
            not league.settings.include_playoffs
            and season.current_week > NFL_REGULAR_SEASON_END
        ):
            return []

        return Game.query.filter_by(
            season_id=season.id,
            week=season.current_week
        ).order_by(
            Game.game_date
        ).all()

    # NBA

    return Game.query.filter(
        Game.season_id == season.id
    ).order_by(
        Game.game_date
    ).all()