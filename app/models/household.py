import uuid

from sqlalchemy import func

from app.extensions import db


class Household(db.Model):
    __tablename__ = "households"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    public_id = db.Column(
        db.Uuid,
        unique=True,
        nullable=False,
        default=uuid.uuid4,
        index=True,
    )

    name = db.Column(
        db.String(160),
        nullable=False,
    )

    default_language = db.Column(
        db.String(5),
        nullable=False,
        default="hu",
    )

    timezone = db.Column(
        db.String(64),
        nullable=False,
        default="Europe/Budapest",
    )

    expiring_soon_days = db.Column(
        db.Integer,
        nullable=False,
        default=5,
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

    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    members = db.relationship(
        "HouseholdMember",
        back_populates="household",
        cascade="all, delete-orphan",
    )
