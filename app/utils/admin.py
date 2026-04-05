from flask_login import current_user
from flask import abort
from functools import wraps


def admin_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if not current_user.is_authenticated:
            abort(403)

        if not current_user.is_admin:
            abort(403)

        return func(*args, **kwargs)

    return wrapper