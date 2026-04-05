from flask import Blueprint, render_template, redirect
from flask_login import login_required
from app.services.espn_service import load_games, update_results, bootstrap_results
from app.models import Game, User, League
from app.extensions import db

admin_bp = Blueprint("admin", __name__)


from flask_login import current_user
from flask import abort
from functools import wraps

def admin_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if not current_user.is_admin:
            abort(403)

        return func(*args, **kwargs)

    return wrapper

# =========================
# ADMIN DASHBOARD
# =========================

@admin_bp.route("/admin")
@login_required
@admin_required
def admin_dashboard():

    games = Game.query.count()
    users = User.query.count()
    leagues = League.query.count()

    live_games = Game.query.filter(
        Game.status != None,
        Game.status != "Scheduled",
        Game.status != "Final"
    ).count()

    return render_template(
        "admin_dashboard.html",
        games=games,
        users=users,
        leagues=leagues,
        live_games=live_games
    )


# =========================
# LOAD GAMES
# =========================

@admin_bp.route("/admin/load_games")
@login_required
@admin_required
def admin_load_games():

    load_games()

    return redirect("/admin")


# =========================
# UPDATE RESULTS
# =========================

@admin_bp.route("/admin/update_results")
@login_required
@admin_required
def admin_update_results():

    update_results()

    return redirect("/admin")


# =========================
# BOOTSTRAP RESULTS
# =========================

@admin_bp.route("/admin/bootstrap_results")
@login_required
@admin_required
def admin_bootstrap():

    bootstrap_results()

    return redirect("/admin")