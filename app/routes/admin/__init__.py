from flask import Blueprint

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)

# =====================================================
# REGISTER ADMIN MODULES
# =====================================================

from . import season
from . import game
from . import league
from . import system