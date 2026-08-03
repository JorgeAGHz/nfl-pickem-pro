"""
=====================================================

NFL Pick'em Pro

Module:
League Queries

Purpose:
Reusable read operations related to leagues.

Responsibilities:
- Retrieve leagues
- Retrieve memberships
- Membership checks
- Ownership checks

Consumers:
- Flask Web
- REST API
- iOS
- Android

=====================================================
"""

from app.models import League, Membership


# =====================================================
# LEAGUE QUERIES
# =====================================================

def get_all_leagues():
    """
    Return all active leagues ordered by name.
    """

    return (
        League.query
        .order_by(League.name)
        .all()
    )


def get_league_by_public_id(public_id):
    """
    Return a league by its public identifier.
    """

    return (
        League.query
        .filter_by(
            public_id=public_id,
            is_archived=False
        )
        .first()
    )


def get_league_by_invite_code(invite_code):
    """
    Return a league by its invitation code.
    """

    return (
        League.query
        .filter_by(
            invite_code=invite_code,
            is_archived=False
        )
        .first()
    )


# =====================================================
# MEMBERSHIP QUERIES
# =====================================================

def get_user_membership(user_id, league_id):
    """
    Return the membership for a user in a league.
    """

    return (
        Membership.query
        .filter_by(
            user_id=user_id,
            league_id=league_id
        )
        .first()
    )


def is_member(user_id, league_id):
    """
    Check whether a user belongs to a league.
    """

    return get_user_membership(
        user_id,
        league_id
    ) is not None


def is_owner(user_id, league):
    """
    Check whether the user owns the league.
    """

    return league.owner_id == user_id