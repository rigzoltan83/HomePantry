import uuid

from flask_login import UserMixin
from sqlalchemy import func

from app.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

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

    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False,
    )

    display_name = db.Column(
        db.String(120),
        nullable=False,
    )

    preferred_language = db.Column(
        db.String(5),
        nullable=False,
        default="hu",
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

    memberships = db.relationship(
        "HouseholdMember",
        back_populates="user",
        cascade="all, delete-orphan",
    )
