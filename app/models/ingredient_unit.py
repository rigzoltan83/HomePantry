from sqlalchemy import UniqueConstraint

from app.extensions import db


class IngredientUnit(db.Model):
    __tablename__ = "ingredient_units"

    __table_args__ = (
        UniqueConstraint(
            "ingredient_id",
            "unit_id",
            name="uq_ingredient_unit",
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

    unit_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "units.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    is_default = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
    )

    sort_order = db.Column(
        db.Integer,
        nullable=False,
        default=100,
    )

    ingredient = db.relationship(
        "Ingredient",
        back_populates="allowed_units",
    )

    unit = db.relationship(
        "Unit",
    )
