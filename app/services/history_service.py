from collections import defaultdict

from app.extensions import db

from app.models import (
    Membership,
    Pick,
    LeagueWeekResult
)

from app.constants import (
    GAME_STATUS_FINAL,
    SEASON_ACTIVE
)

from app.services.pick_service import (
    get_current_week_games
)

from app.services.scoring_service import (
    calculate_correct_picks,
    calculate_points
)


# =====================================================
# CLOSE WEEK
# =====================================================

def close_week(
    league
):

    season = league.season

    if season.status != SEASON_ACTIVE:

        raise ValueError(
            "Season is not active."
        )

    week = season.current_week

    if week is None:

        raise ValueError(
            "No active week."
        )

    existing = LeagueWeekResult.query.filter_by(

        league_id=league.id,

        week=week

    ).first()

    if existing:

        raise ValueError(
            f"Week {week} is already closed."
        )

    games = get_current_week_games(
        league
    )

    if not games:

        raise ValueError(
            "No games found for current week."
        )

    for game in games:

        if game.status != GAME_STATUS_FINAL:

            raise ValueError(
                "Cannot close week. "
                "All games must be final."
            )

    return calculate_week_results(

        league=league,

        week=week,

        games=games

    )


# =====================================================
# CALCULATE WEEK RESULTS
# =====================================================

def calculate_week_results(
    league,
    week,
    games
):

    memberships = Membership.query.filter_by(
        league_id=league.id
    ).all()

    game_ids = [
        game.id
        for game in games
    ]

    user_scores = []

    for membership in memberships:

        user_id = membership.user_id

        picks = Pick.query.filter(

            Pick.league_id == league.id,

            Pick.user_id == user_id,

            Pick.game_id.in_(game_ids)

        ).all()

        correct_picks = calculate_correct_picks(

            league,

            picks

        )

        points = calculate_points(

            league,

            picks

        )

        user_scores.append({

            "user_id": user_id,

            "correct_picks": correct_picks,

            "points": points

        })

    ranked_scores = build_rankings(
        user_scores
    )

    results = []

    for row in ranked_scores:

        result = LeagueWeekResult(

            league_id=league.id,

            season_id=league.season.id,

            user_id=row["user_id"],

            week=week,

            correct_picks=row[
                "correct_picks"
            ],

            points=row[
                "points"
            ],

            rank=row[
                "rank"
            ]
        )

        db.session.add(result)

        results.append(result)

    db.session.commit()

    return results


# =====================================================
# COMPETITION RANKING
# =====================================================

def build_rankings(
    rows
):

    sorted_rows = sorted(

        rows,

        key=lambda x: x["points"],

        reverse=True

    )

    current_rank = 1

    previous_points = None

    for index, row in enumerate(
        sorted_rows
    ):

        if previous_points is None:

            row["rank"] = current_rank

        elif row["points"] == previous_points:

            row["rank"] = current_rank

        else:

            current_rank = index + 1

            row["rank"] = current_rank

        previous_points = row["points"]

    return sorted_rows


# =====================================================
# HISTORY
# =====================================================

def get_history(
    league
):

    return LeagueWeekResult.query.filter_by(

        league_id=league.id

    ).order_by(

        LeagueWeekResult.week.asc()

    ).all()


# =====================================================
# OFFICIAL LEADERBOARD
# =====================================================

def get_official_leaderboard(
    league
):

    rows = LeagueWeekResult.query.filter_by(
        league_id=league.id
    ).all()

    totals = defaultdict(

        lambda: {

            "points": 0,

            "correct_picks": 0

        }

    )

    for row in rows:

        totals[row.user_id][
            "points"
        ] += row.points

        totals[row.user_id][
            "correct_picks"
        ] += row.correct_picks

    leaderboard = []

    for user_id, values in totals.items():

        leaderboard.append({

            "user_id": user_id,

            "points": values[
                "points"
            ],

            "correct_picks": values[
                "correct_picks"
            ]

        })

    return build_rankings(
        leaderboard
    )