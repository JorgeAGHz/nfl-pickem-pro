from flask import jsonify

from flask_login import (
    login_required,
    current_user
)

from app.routes.admin import admin_bp

from app.services.season import (
    get_all_seasons,
    activate_season,
)

from app.services.game.queries import (
    get_games_by_season,
)


# =====================================================
# GAMES
# =====================================================

@admin_bp.route("/games")
@login_required
def games():

    if not current_user.is_admin:
        return "Forbidden", 403

    seasons = get_all_seasons()

    return jsonify([
        {
            "id": season.id,
            "sport": season.sport,
            "year": season.year,
            "status": season.status,
            "current_week": season.current_week
        }
        for season in seasons
    ])


# =====================================================
# TEST - ACTIVATE SEASON
# =====================================================

@admin_bp.route("/games/test/activate/<int:season_id>")
@login_required
def test_activate(
    season_id
):

    if not current_user.is_admin:
        return "Forbidden", 403

    activate_season(
        season_id
    )

    return jsonify({
        "success": True
    })


# =====================================================
# TEST - GAMES
# =====================================================

@admin_bp.route("/games/test/<int:season_id>")
@login_required
def test_games(
    season_id
):

    if not current_user.is_admin:
        return "Forbidden", 403

    games = get_games_by_season(
        season_id
    )

    return jsonify([
        {
            "id": game.id,
            "week": game.week,
            "home": game.home_team,
            "away": game.away_team,
            "status": game.status
        }
        for game in games
    ])