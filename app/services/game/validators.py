from app.constants import (
    GAME_STATUS_SCHEDULED,
    GAME_STATUS_IN_PROGRESS,
    GAME_STATUS_FINAL,
    SEASON_TYPE_REGULAR,
    SEASON_TYPE_PLAYOFF,
)


# =====================================================
# IMPORT
# =====================================================

def can_import_schedule(season):

    return season.status != "CLOSED"


# =====================================================
# SCORES
# =====================================================

def can_update_scores(game):

    return game.status in (
        GAME_STATUS_SCHEDULED,
        GAME_STATUS_IN_PROGRESS,
        GAME_STATUS_FINAL,
    )


# =====================================================
# WEEK
# =====================================================

def validate_week(week):

    return week is not None and week >= 1


# =====================================================
# SEASON TYPE
# =====================================================

def validate_season_type(season_type):

    return season_type in (
        SEASON_TYPE_REGULAR,
        SEASON_TYPE_PLAYOFF,
    )


# =====================================================
# GAME
# =====================================================

def validate_game(parsed_game):

    if not parsed_game.api_id:
        return False

    if not parsed_game.home_team:
        return False

    if not parsed_game.away_team:
        return False

    if not validate_week(parsed_game.week):
        return False

    if not validate_season_type(
        parsed_game.season_type
    ):
        return False

    return True