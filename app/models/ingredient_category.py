import uuid

from sqlalchemy import UniqueConstraint
from sqlalchemy import func

from app.extensions import db


class IngredientCategory(db.Model):
    __tablename__ = "ingredient_categories"

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

    canonical_key = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
        index=True,
    )

    parent_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "ingredient_categories.id",
            ondelete="RESTRICT",
        ),
        nullable=True,
        index=True,
    )

    sort_order = db.Column(
        db.Integer,
        nullable=False,
        default=100,
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

    parent = db.relationship(
        "IngredientCategory",
        remote_side=[id],
        back_populates="children",
    )

    children = db.relationship(
        "IngredientCategory",
        back_populates="parent",
    )

    translations = db.relationship(
        "IngredientCategoryTranslation",
        back_populates="category",
        cascade="all, delete-orphan",
    )


class IngredientCategoryTranslation(db.Model):
    __tablename__ = (
        "ingredient_category_translations"
    )

    __table_args__ = (
        UniqueConstraint(
            "category_id",
            "language_code",
            name=(
                "uq_ingredient_category_translation"
            ),
        ),
    )

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "ingredient_categories.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    language_code = db.Column(
        db.String(5),
        nullable=False,
        index=True,
    )

    name = db.Column(
        db.String(160),
        nullable=False,
    )

    category = db.relationship(
        "IngredientCategory",
        back_populates="translations",
    )
