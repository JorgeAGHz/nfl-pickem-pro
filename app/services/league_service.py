import secrets
import string
import uuid

from datetime import datetime

from app.extensions import db

from app.models import (
    League,
    LeagueSettings,
    Membership,
    User
)

from app.constants import (
    ROLE_OWNER,
    ROLE_MEMBER
)


# =====================================================
# INVITE CODE
# =====================================================

def generate_invite_code(
    length=8
):

    alphabet = (
        string.ascii_uppercase +
        string.digits
    )

    while True:

        code = "".join(

            secrets.choice(alphabet)

            for _ in range(length)

        )

        exists = League.query.filter_by(
            invite_code=code
        ).first()

        if not exists:

            return code


# =====================================================
# PUBLIC ID
# =====================================================

def generate_public_id():

    return str(
        uuid.uuid4()
    )


# =====================================================
# CREATE LEAGUE
# =====================================================

def create_league(

    owner,

    season,

    name,

    pick_mode,

    include_playoffs,

    visibility

):

    existing = League.query.filter_by(

        season_id=season.id,

        name=name

    ).first()

    if existing:

        raise ValueError(
            "League name already exists "
            "for this season."
        )

    league = League(

        public_id=generate_public_id(),

        name=name,

        season_id=season.id,

        owner_id=owner.id,

        invite_code=generate_invite_code()

    )

    db.session.add(
        league
    )

    db.session.flush()

    settings = LeagueSettings(

        league_id=league.id,

        pick_mode=pick_mode,

        include_playoffs=include_playoffs,

        visibility=visibility

    )

    db.session.add(
        settings
    )

    membership = Membership(

        user_id=owner.id,

        league_id=league.id,

        role=ROLE_OWNER

    )

    db.session.add(
        membership
    )

    db.session.commit()

    return league


# =====================================================
# JOIN LEAGUE
# =====================================================

def join_league(

    user,

    invite_code

):

    league = League.query.filter_by(

        invite_code=invite_code,

        is_archived=False

    ).first()

    if not league:

        raise ValueError(
            "Invalid invite code."
        )

    existing = Membership.query.filter_by(

        user_id=user.id,

        league_id=league.id

    ).first()

    if existing:

        raise ValueError(
            "Already a member."
        )

    current_members = Membership.query.filter_by(
        league_id=league.id
    ).count()

    if (

        current_members >=
        league.settings.max_players

    ):

        raise ValueError(
            "League is full."
        )

    membership = Membership(

        user_id=user.id,

        league_id=league.id,

        role=ROLE_MEMBER

    )

    db.session.add(
        membership
    )

    db.session.commit()

    return league


# =====================================================
# TRANSFER OWNERSHIP
# =====================================================

def transfer_ownership(

    league,

    new_owner_id

):

    membership = Membership.query.filter_by(

        league_id=league.id,

        user_id=new_owner_id

    ).first()

    if not membership:

        raise ValueError(
            "User is not a member."
        )

    old_owner = Membership.query.filter_by(

        league_id=league.id,

        role=ROLE_OWNER

    ).first()

    if not old_owner:

        raise ValueError(
            "Owner not found."
        )

    old_owner.role = ROLE_MEMBER

    membership.role = ROLE_OWNER

    league.owner_id = new_owner_id

    db.session.commit()

    return league


# =====================================================
# LEAVE LEAGUE
# =====================================================

def leave_league(

    league,

    user

):

    membership = Membership.query.filter_by(

        league_id=league.id,

        user_id=user.id

    ).first()

    if not membership:

        raise ValueError(
            "Membership not found."
        )

    if membership.role == ROLE_OWNER:

        raise ValueError(
            "Owner must transfer "
            "ownership first."
        )

    db.session.delete(
        membership
    )

    db.session.flush()

    remaining_members = Membership.query.filter_by(
        league_id=league.id
    ).count()

    if remaining_members == 0:

        archive_league(
            league
        )

    db.session.commit()

    return True


# =====================================================
# ARCHIVE LEAGUE
# =====================================================

def archive_league(
    league
):

    league.is_archived = True

    league.archived_at = datetime.utcnow()

    db.session.commit()

    return league


# =====================================================
# REGENERATE INVITE CODE
# =====================================================

def regenerate_invite_code(
    league
):

    league.invite_code = (
        generate_invite_code()
    )

    db.session.commit()

    return league.invite_code


# =====================================================
# LOOKUPS
# =====================================================

def get_league_by_public_id(
    public_id
):

    return League.query.filter_by(

        public_id=public_id,

        is_archived=False

    ).first()


def get_user_membership(

    league_id,

    user_id

):

    return Membership.query.filter_by(

        league_id=league_id,

        user_id=user_id

    ).first()


def is_member(

    league_id,

    user_id

):

    return (

        get_user_membership(

            league_id,

            user_id

        )

        is not None

    )


def is_owner(

    league_id,

    user_id

):

    membership = get_user_membership(

        league_id,

        user_id

    )

    if not membership:

        return False

    return membership.role == ROLE_OWNER

# =====================================================
# INVITATION PREVIEW
# =====================================================

def get_league_preview_by_invite(invite_code):
    """
    Return the information required to preview
    a league before joining.
    """

    league = League.query.filter_by(
        invite_code=invite_code,
        is_archived=False
    ).first()

    if not league:
        return None

    member_count = Membership.query.filter_by(
        league_id=league.id
    ).count()

    return {
        "league": league,
        "member_count": member_count
    }