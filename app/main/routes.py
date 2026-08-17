from flask import render_template
from flask_login import (
    current_user,
    login_required,
)
from sqlalchemy import select

from app.extensions import db
from app.models import HouseholdMember

from . import bp


@bp.get("/")
@login_required
def index():
    membership = db.session.scalar(
        select(HouseholdMember)
        .where(
            HouseholdMember.user_id
            == current_user.id,
            HouseholdMember.is_active.is_(
                True
            ),
        )
        .order_by(
            HouseholdMember.id
        )
    )

    household = (
        membership.household
        if membership is not None
        else None
    )

    return render_template(
        "main/index.html",
        household=household,
        membership=membership,
    )
