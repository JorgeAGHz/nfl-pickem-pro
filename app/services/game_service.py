from app.models import Game


def get_game_by_api_id(
    api_id
):

    return Game.query.filter_by(
        api_id=api_id
    ).first()