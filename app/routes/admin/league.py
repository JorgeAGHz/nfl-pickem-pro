from flask import render_template

from flask_login import (
    login_required,
    current_user
)

from app.routes.admin import admin_bp

from app.services.league import (
    get_all_leagues,
)


@admin_bp.route("/leagues")
@login_required
def leagues():

    if not current_user.is_admin:
        return "Forbidden", 403

    leagues = get_all_leagues()

    return render_template(
        "admin/leagues.html",
        leagues=leagues
    )