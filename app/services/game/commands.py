from app.extensions import db
from app.models import Game

from app.services.game.validators import (
    validate_game,
)

from app.services.game.queries import (
    get_game_by_api_id,
)

from app.services.game.exceptions import (
    InvalidGameError,
)

from app.providers.espn.models import ParsedGame


# =====================================================
# INTERNAL
# =====================================================

def _upsert_game(
    season,
    parsed_game: ParsedGame
):
    """
    Creates or updates a game.

    Does NOT commit.
    """

    if not validate_game(parsed_game):
        raise InvalidGameError(
            f"Invalid game: {parsed_game.api_id}"
        )

    game = get_game_by_api_id(
        season.id,
        parsed_game.api_id
    )

    if game is None:

        game = Game(

            season_id=season.id,

            api_id=parsed_game.api_id,

            season_type=parsed_game.season_type,

            week=parsed_game.week,

            game_date=parsed_game.game_date,

            home_team=parsed_game.home_team,

            away_team=parsed_game.away_team,

            home_abbr=parsed_game.home_abbr,

            away_abbr=parsed_game.away_abbr,

            home_logo=parsed_game.home_logo,

            away_logo=parsed_game.away_logo,

            spread=parsed_game.spread,

            home_score=parsed_game.home_score,

            away_score=parsed_game.away_score,

            status=parsed_game.status,

            clock=parsed_game.clock,

            period=parsed_game.period

        )

        db.session.add(game)

        return game

    game.game_date = parsed_game.game_date

    game.week = parsed_game.week

    game.season_type = parsed_game.season_type

    game.home_team = parsed_game.home_team
    game.away_team = parsed_game.away_team

    game.home_abbr = parsed_game.home_abbr
    game.away_abbr = parsed_game.away_abbr

    game.home_logo = parsed_game.home_logo
    game.away_logo = parsed_game.away_logo

    game.spread = parsed_game.spread

    game.home_score = parsed_game.home_score
    game.away_score = parsed_game.away_score

    game.status = parsed_game.status
    game.clock = parsed_game.clock
    game.period = parsed_game.period

    return game


# =====================================================
# IMPORT SCHEDULE
# =====================================================

def import_schedule(
    season,
    provider
):
    """
    Imports or updates
    every game for one week.

    One commit only.
    """

    parsed_games = provider.import_schedule(

        year=season.year,

        week=season.current_week

    )

    imported = []

    for parsed_game in parsed_games:

        game = _upsert_game(

            season,

            parsed_game

        )

        imported.append(game)

    db.session.commit()

    return imported


# =====================================================
# SYNC SCORES
# =====================================================

def sync_scores(
    season,
    provider
):
    """
    Synchronizes scores and
    game status.

    One commit only.
    """

    parsed_games = provider.update_scores()

    updated = []

    for parsed_game in parsed_games:

        game = get_game_by_api_id(

            season.id,

            parsed_game.api_id

        )

        if game is None:
            continue

        game.home_score = parsed_game.home_score
        game.away_score = parsed_game.away_score

        game.status = parsed_game.status
        game.clock = parsed_game.clock
        game.period = parsed_game.period

        updated.append(game)

    db.session.commit()

    return updated