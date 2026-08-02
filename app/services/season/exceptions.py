# =====================================================
# BASE
# =====================================================

class SeasonError(Exception):
    """
    Base exception for
    the Season domain.
    """
    pass


# =====================================================
# CREATE
# =====================================================

class SeasonAlreadyExistsError(
    SeasonError
):
    pass


class InvalidSportError(
    SeasonError
):
    pass


class InvalidYearError(
    SeasonError
):
    pass


# =====================================================
# TRANSITIONS
# =====================================================

class InvalidSeasonTransitionError(
    SeasonError
):
    pass


class SeasonNotFoundError(
    SeasonError
):
    pass


# =====================================================
# WEEK
# =====================================================

class InvalidWeekError(
    SeasonError
):
    pass