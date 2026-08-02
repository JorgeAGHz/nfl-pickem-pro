from collections import defaultdict

from app.extensions import db

from app.models import (
    User,
    Membership,
    Pick
)

from app.constants import (

    GAME_STATUS_FINAL,

    SELECTION_HOME,
    SELECTION_AWAY,
    SELECTION_DIFFERENCE

)

from app.services.pick_service import (

    can_view_pick,
    get_current_week_games

)

from app.services.scoring_service import (
    is_pick_correct
)


# =====================================================
# LIVE CONTEXT
# =====================================================

def build_live_context(
    league,
    viewer_id
):

    games = get_current_week_games(
        league
    )

    memberships = Membership.query.filter_by(
        league_id=league.id
    ).all()

    users = []

    for membership in memberships:

        user = db.session.get(
            User,
            membership.user_id
        )

        if user:

            users.append(user)

    all_picks = Pick.query.filter_by(
        league_id=league.id
    ).all()

    pick_map = {

        (
            pick.user_id,
            pick.game_id
        ): pick

        for pick in all_picks

    }

    live_matrix = {}

    scores = defaultdict(int)

    pick_distribution = {}

    # =================================================
    # PICK DISTRIBUTION
    # =================================================

    for game in games:

        counts = {

            SELECTION_HOME: 0,

            SELECTION_AWAY: 0,

            SELECTION_DIFFERENCE: 0

        }

        for pick in all_picks:

            if pick.game_id != game.id:
                continue

            if pick.selection in counts:

                counts[
                    pick.selection
                ] += 1

        pick_distribution[
            game.id
        ] = counts

    # =================================================
    # CLUTCH GAME
    # =================================================

    clutch_game = None

    clutch_count = -1

    for game in games:

        counts = pick_distribution.get(
            game.id,
            {}
        )

        total = sum(
            counts.values()
        )

        if total > clutch_count:

            clutch_count = total

            clutch_game = game.id

    # =================================================
    # LIVE MATRIX
    # =================================================

    for user in users:

        live_matrix[user.id] = {}

        live_score = 0

        for game in games:

            pick = pick_map.get(

                (
                    user.id,
                    game.id
                )

            )

            # ---------------------------------
            # NO PICK
            # ---------------------------------

            if not pick:

                live_matrix[user.id][
                    game.id
                ] = {

                    "selection": None,

                    "correct": None,

                    "visible": False

                }

                continue

            # ---------------------------------
            # VISIBILITY
            # ---------------------------------

            visible = can_view_pick(

                game,

                viewer_id,

                user.id

            )

            if not visible:

                live_matrix[user.id][
                    game.id
                ] = {

                    "selection": None,

                    "correct": None,

                    "visible": False

                }

                continue

            # ---------------------------------
            # RESULT
            # ---------------------------------

            correct = None

            if (
                game.status ==
                GAME_STATUS_FINAL
            ):

                correct = is_pick_correct(

                    league,

                    game,

                    pick.selection

                )

                if correct:

                    live_score += 1

            live_matrix[user.id][
                game.id
            ] = {

                "selection": pick.selection,

                "correct": correct,

                "visible": True

            }

        scores[user.id] = live_score

    return {

        "games": games,

        "users": users,

        "matrix": live_matrix,

        "scores": dict(scores),

        "pick_distribution":
            pick_distribution,

        "clutch_game":
            clutch_game

    }