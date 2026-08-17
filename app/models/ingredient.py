import uuid

from sqlalchemy import UniqueConstraint
from sqlalchemy import func

from app.extensions import db


class Ingredient(db.Model):
    __tablename__ = "ingredients"

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
        db.String(160),
        unique=True,
        nullable=False,
        index=True,
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "ingredient_categories.id",
            ondelete="RESTRICT",
        ),
        nullable=True,
        index=True,
    )

    default_unit_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "units.id",
            ondelete="RESTRICT",
        ),
        nullable=True,
        index=True,
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

    category = db.relationship(
        "IngredientCategory",
    )

    default_unit = db.relationship(
        "Unit",
    )

    translations = db.relationship(
        "IngredientTranslation",
        back_populates="ingredient",
        cascade="all, delete-orphan",
    )

    aliases = db.relationship(
        "IngredientAlias",
        back_populates="ingredient",
        cascade="all, delete-orphan",
    )

    substitutions_from = db.relationship(
        "IngredientSubstitution",
        foreign_keys=(
            "IngredientSubstitution."
            "source_ingredient_id"
        ),
        back_populates="source_ingredient",
        cascade="all, delete-orphan",
    )

    substitutions_to = db.relationship(
        "IngredientSubstitution",
        foreign_keys=(
            "IngredientSubstitution."
            "target_ingredient_id"
        ),
        back_populates="target_ingredient",
        cascade="all, delete-orphan",
    )


class IngredientTranslation(db.Model):
    __tablename__ = "ingredient_translations"

    __table_args__ = (
        UniqueConstraint(
            "ingredient_id",
            "language_code",
            name="uq_ingredient_translation",
        ),
    )

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    ingredient_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "ingredients.id",
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
        db.String(200),
        nullable=False,
    )

    ingredient = db.relationship(
        "Ingredient",
        back_populates="translations",
    )


class IngredientAlias(db.Model):
    __tablename__ = "ingredient_aliases"

    __table_args__ = (
        UniqueConstraint(
            "ingredient_id",
            "language_code",
            "normalized_alias",
            name="uq_ingredient_alias",
        ),
    )

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    ingredient_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "ingredients.id",
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

    alias = db.Column(
        db.String(200),
        nullable=False,
    )

    normalized_alias = db.Column(
        db.String(200),
        nullable=False,
        index=True,
    )

    ingredient = db.relationship(
        "Ingredient",
        back_populates="aliases",
    )
