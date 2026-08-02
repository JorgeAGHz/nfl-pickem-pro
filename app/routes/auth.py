from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    login_required
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from app.extensions import db

from app.models import User


auth_bp = Blueprint(
    "auth",
    __name__
)


# =====================================================
# LOGIN
# =====================================================

@auth_bp.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        user = User.query.filter_by(
            email=email
        ).first()

        if not user:

            flash(
                "Invalid credentials.",
                "danger"
            )

            return render_template(
                "login.html"
            )

        if not check_password_hash(

            user.password_hash,

            password

        ):

            flash(
                "Invalid credentials.",
                "danger"
            )

            return render_template(
                "login.html"
            )

        login_user(user)

        return redirect(
            url_for(
                "league.dashboard"
            )
        )

    return render_template(
        "login.html"
    )


# =====================================================
# REGISTER
# =====================================================

@auth_bp.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            flash(
                "Email already registered.",
                "danger"
            )

            return render_template(
                "register.html"
            )

        is_first_user = (

            User.query.count() == 0

        )

        user = User(

            name=name,

            email=email,

            password_hash=generate_password_hash(
                password
            ),

            is_admin=is_first_user

        )

        db.session.add(user)

        db.session.commit()

        flash(
            "Account created successfully.",
            "success"
        )

        return redirect(
            url_for(
                "auth.login"
            )
        )

    return render_template(
        "register.html"
    )


# =====================================================
# LOGOUT
# =====================================================

@auth_bp.route(
    "/logout"
)
@login_required
def logout():

    logout_user()

    return redirect(
        url_for(
            "auth.login"
        )
    )