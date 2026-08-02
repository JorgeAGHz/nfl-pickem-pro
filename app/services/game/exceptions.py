# =====================================================
# BASE
# =====================================================

class GameError(Exception):
    """
    Base exception for
    the Game domain.
    """
    pass


# =====================================================
# NOT FOUND
# =====================================================

class GameNotFoundError(
    GameError
):
    pass


# =====================================================
# DUPLICATES
# =====================================================

class DuplicateGameError(
    GameError
):
    pass


# =====================================================
# VALIDATION
# =====================================================

class InvalidGameError(
    GameError
):
    pass


class InvalidWeekError(
    GameError
):
    pass


class InvalidSeasonTypeError(
    GameError
):
    pass


class ImportScheduleError(
    GameError
):
    pass