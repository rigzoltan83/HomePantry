import uuid

from sqlalchemy import UniqueConstraint
from sqlalchemy import func

from app.extensions import db


class IngredientSubstitution(db.Model):
    __tablename__ = "ingredient_substitutions"

    __table_args__ = (
        UniqueConstraint(
            "source_ingredient_id",
            "target_ingredient_id",
            "context",
            name="uq_ingredient_substitution",
        ),
    )

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

    source_ingredient_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "ingredients.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    target_ingredient_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "ingredients.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    rating = db.Column(
        db.String(20),
        nullable=False,
        default="acceptable",
        index=True,
    )

    quantity_ratio = db.Column(
        db.Numeric(
            precision=12,
            scale=6,
        ),
        nullable=False,
        default=1,
    )

    context = db.Column(
        db.String(40),
        nullable=False,
        default="general",
        index=True,
    )

    note_hu = db.Column(
        db.Text,
        nullable=True,
    )

    note_en = db.Column(
        db.Text,
        nullable=True,
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

    source_ingredient = db.relationship(
        "Ingredient",
        foreign_keys=[
            source_ingredient_id
        ],
        back_populates="substitutions_from",
    )

    target_ingredient = db.relationship(
        "Ingredient",
        foreign_keys=[
            target_ingredient_id
        ],
        back_populates="substitutions_to",
    )
