from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

from app.models import User, Membership, Invite
from app.extensions import db


# =========================
# BLUEPRINT
# =========================

auth_bp = Blueprint("auth", __name__)


# =========================
# LOGIN
# =========================

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            login_user(user)

            pending = session.pop("pending_invite", None)

            if pending:
                invite = Invite.query.filter_by(token=pending).first()

                if invite:

                    existing = Membership.query.filter_by(
                        user_id=user.id,
                        league_id=invite.league_id
                    ).first()

                    if not existing:
                        membership = Membership(
                            user_id=user.id,
                            league_id=invite.league_id
                        )

                        db.session.add(membership)

                    db.session.delete(invite)
                    db.session.commit()

            return redirect("/")

    return render_template("login.html")


# =========================
# REGISTER
# =========================

@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return "Este correo ya está registrado. Intenta iniciar sesión."

        hashed = generate_password_hash(password)
        
        admin_exists = User.query.filter_by(is_admin=True).first()
        if not admin_exists:
            is_admin = True
        else:
            is_admin = False

        user = User(
            name=name,
            email=email,
            password=hashed,
            is_admin=is_admin
        )
        


        db.session.add(user)
        db.session.commit()

        # =========================
        # JOIN LEAGUE IF INVITED
        # =========================

        token = session.pop("invite_token", None)

        if token:

            invite = Invite.query.filter_by(token=token).first()

            if invite and not invite.used:

                membership = Membership(
                    user_id=user.id,
                    league_id=invite.league_id
                )

                db.session.add(membership)

                invite.used = True

                db.session.commit()

                return redirect(f"/league/{invite.league_id}")

        return redirect("/login")

    return render_template("register.html")

# =========================
# LOGOUT
# =========================

@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect("/login")