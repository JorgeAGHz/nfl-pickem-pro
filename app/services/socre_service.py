from sqlalchemy import func
from app.models import Pick, Game
from app.extensions import db


def get_league_scores(league_id):

    scores = db.session.query(
        Pick.user_id,
        func.sum(
            func.case(
                (
                    Pick.choice == Game.result,
                    1
                ),
                else_=0
            )
        ).label("points")
    ).join(Game, Game.id == Pick.game_id
    ).filter(
        Pick.league_id == league_id,
        Game.result != None
    ).group_by(
        Pick.user_id
    ).all()

    return {s.user_id: s.points for s in scores}