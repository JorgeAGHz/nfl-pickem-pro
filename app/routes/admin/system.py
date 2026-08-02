from flask_login import (
    login_required,
    current_user
)

from app.routes.admin import admin_bp


@admin_bp.route("/")
@login_required
def dashboard():

    if not current_user.is_admin:
        return "Forbidden", 403

    return "Administration"