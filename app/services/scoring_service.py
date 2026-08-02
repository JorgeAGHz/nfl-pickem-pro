from app.constants import (

    PICK_MODE_NFL_SPREAD,
    PICK_MODE_NFL_WINNER,
    PICK_MODE_NBA_WINNER,

    GAME_STATUS_FINAL,

    SELECTION_HOME,
    SELECTION_AWAY,
    SELECTION_DIFFERENCE
)


# =====================================================
# GAME STATUS
# =====================================================

def game_is_final(game):

    return (
        game.status ==
        GAME_STATUS_FINAL
    )


# =====================================================
# PUBLIC API
# =====================================================

def is_pick_correct(
    league,
    game,
    selection
):
    """
    Returns True if the selection
    is correct for the given game.
    """

    winner = get_winning_selection(
        league,
        game
    )

    if winner is None:
        return False

    return selection == winner


def get_winning_selection(
    league,
    game
):
    """
    Returns:

    HOME
    AWAY
    DIFFERENCE

    or None if the game
    is not final.
    """

    pick_mode = league.settings.pick_mode

    if pick_mode == PICK_MODE_NFL_SPREAD:

        return get_nfl_spread_winner(
            game
        )

    if pick_mode == PICK_MODE_NFL_WINNER:

        return get_nfl_winner(
            game
        )

    if pick_mode == PICK_MODE_NBA_WINNER:

        return get_nba_winner(
            game
        )

    return None


# =====================================================
# NFL SPREAD
# =====================================================

def score_nfl_spread(
    game,
    selection
):
    """
    Legacy helper.
    """

    winner = get_nfl_spread_winner(
        game
    )

    if winner is None:
        return False

    return selection == winner


def get_nfl_spread_winner(
    game
):
    """
    Rules:

    HOME
        Home wins by 7 or more

    AWAY
        Away wins by 7 or more

    DIFFERENCE
        Margin less than 7
    """

    if not game_is_final(game):
        return None

    if game.home_score is None:
        return None

    if game.away_score is None:
        return None

    home_score = game.home_score
    away_score = game.away_score

    margin = abs(
        home_score - away_score
    )

    # Less than 7 points

    if margin < 7:

        return SELECTION_DIFFERENCE

    # 7 or more

    if home_score > away_score:

        return SELECTION_HOME

    return SELECTION_AWAY


# =====================================================
# NFL WINNER
# =====================================================

def score_nfl_winner(
    game,
    selection
):
    """
    Legacy helper.
    """

    winner = get_nfl_winner(
        game
    )

    if winner is None:
        return False

    return selection == winner


def get_nfl_winner(
    game
):
    """
    HOME
        Home wins

    AWAY
        Away wins

    Tie
        Nobody wins
    """

    if not game_is_final(game):
        return None

    if game.home_score is None:
        return None

    if game.away_score is None:
        return None

    home_score = game.home_score
    away_score = game.away_score

    if home_score == away_score:

        return None

    if home_score > away_score:

        return SELECTION_HOME

    return SELECTION_AWAY


# =====================================================
# NBA WINNER
# =====================================================

def score_nba_winner(
    game,
    selection
):
    """
    Legacy helper.
    """

    winner = get_nba_winner(
        game
    )

    if winner is None:
        return False

    return selection == winner


def get_nba_winner(
    game
):
    """
    HOME
        Home wins

    AWAY
        Away wins
    """

    if not game_is_final(game):
        return None

    if game.home_score is None:
        return None

    if game.away_score is None:
        return None

    if game.home_score > game.away_score:

        return SELECTION_HOME

    return SELECTION_AWAY


# =====================================================
# UTILITIES
# =====================================================

def game_has_final_score(
    game
):
    """
    Returns True when the game
    is final and both scores exist.
    """

    return (

        game_is_final(game)

        and

        game.home_score is not None

        and

        game.away_score is not None

    )


# =====================================================
# CORRECT PICKS
# =====================================================

def calculate_correct_picks(
    league,
    picks
):
    """
    Returns total correct picks.
    """

    total = 0

    for pick in picks:

        if is_pick_correct(
            league,
            pick.game,
            pick.selection
        ):
            total += 1

    return total


# =====================================================
# POINTS
# =====================================================

def calculate_points(
    league,
    picks
):
    """
    For V2 points and correct picks
    are currently equivalent.

    Future scoring systems may
    award bonus points.
    """

    return calculate_correct_picks(
        league,
        picks
    )