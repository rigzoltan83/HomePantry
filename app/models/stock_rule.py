import uuid

from sqlalchemy import UniqueConstraint
from sqlalchemy import func

from app.extensions import db


class StockRule(db.Model):
    __tablename__ = "stock_rules"

    __table_args__ = (
        UniqueConstraint(
            "household_id",
            "ingredient_id",
            name="uq_stock_rule_household_ingredient",
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

    household_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "households.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
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

    minimum_quantity = db.Column(
        db.Numeric(
            precision=18,
            scale=6,
        ),
        nullable=False,
    )

    unit_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "units.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True,
        index=True,
    )

    note = db.Column(
        db.Text,
        nullable=True,
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

    household = db.relationship(
        "Household",
    )

    ingredient = db.relationship(
        "Ingredient",
    )

    unit = db.relationship(
        "Unit",
    )
