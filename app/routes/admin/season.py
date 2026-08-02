from flask import (
    render_template,
    redirect,
    request,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from app.routes.admin import admin_bp

from app.services.season import (
    get_all_seasons,
    create_season,
    activate_season,
    close_season
)


# =====================================================
# ADMIN SEASONS
# =====================================================

@admin_bp.route("/seasons")
@login_required
def seasons():

    if not current_user.is_admin:
        return "Forbidden", 403

    seasons = get_all_seasons()

    return render_template(
        "admin/seasons.html",
        seasons=seasons
    )


# =====================================================
# CREATE
# =====================================================

@admin_bp.route(
    "/seasons/create",
    methods=["POST"]
)
@login_required
def create():

    if not current_user.is_admin:
        return "Forbidden", 403

    try:

        sport = request.form["sport"]
        year = int(
            request.form["year"]
        )

        create_season(
            sport,
            year
        )

        flash(
            "Season created successfully.",
            "success"
        )

    except Exception as exc:

        flash(
            str(exc),
            "error"
        )

    return redirect(
        "/admin/seasons"
    )


# =====================================================
# ACTIVATE
# =====================================================

@admin_bp.route(
    "/seasons/<int:season_id>/activate",
    methods=["POST"]
)
@login_required
def activate(
    season_id
):

    if not current_user.is_admin:
        return "Forbidden", 403

    try:

        activate_season(
            season_id
        )

        flash(
            "Season activated.",
            "success"
        )

    except Exception as exc:

        flash(
            str(exc),
            "error"
        )

    return redirect(
        "/admin/seasons"
    )


# =====================================================
# CLOSE
# =====================================================

@admin_bp.route(
    "/seasons/<int:season_id>/close",
    methods=["POST"]
)
@login_required
def close(
    season_id
):

    if not current_user.is_admin:
        return "Forbidden", 403

    try:

        close_season(
            season_id
        )

        flash(
            "Season closed.",
            "success"
        )

    except Exception as exc:

        flash(
            str(exc),
            "error"
        )

    return redirect(
        "/admin/seasons"
    )