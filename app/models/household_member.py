from sqlalchemy import UniqueConstraint
from sqlalchemy import func

from app.extensions import db


class HouseholdMember(db.Model):
    __tablename__ = "household_members"

    __table_args__ = (
        UniqueConstraint(
            "household_id",
            "user_id",
            name="uq_household_member_user",
        ),
    )

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    household_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "households.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    role = db.Column(
        db.String(20),
        nullable=False,
        default="member",
    )

    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True,
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    household = db.relationship(
        "Household",
        back_populates="members",
    )

    user = db.relationship(
        "User",
        back_populates="memberships",
    )
