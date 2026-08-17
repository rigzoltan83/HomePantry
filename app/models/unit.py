from decimal import Decimal

from sqlalchemy import UniqueConstraint

from app.extensions import db


class Unit(db.Model):
    __tablename__ = "units"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    code = db.Column(
        db.String(30),
        unique=True,
        nullable=False,
        index=True,
    )

    dimension = db.Column(
        db.String(20),
        nullable=False,
        index=True,
    )

    system = db.Column(
        db.String(20),
        nullable=False,
        default="metric",
        index=True,
    )

    symbol = db.Column(
        db.String(20),
        nullable=False,
    )

    factor_to_base = db.Column(
        db.Numeric(
            precision=24,
            scale=12,
        ),
        nullable=False,
        default=Decimal("1"),
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

    translations = db.relationship(
        "UnitTranslation",
        back_populates="unit",
        cascade="all, delete-orphan",
    )


class UnitTranslation(db.Model):
    __tablename__ = "unit_translations"

    __table_args__ = (
        UniqueConstraint(
            "unit_id",
            "language_code",
            name="uq_unit_translation",
        ),
    )

    id = db.Column(
        db.Integer,
        primary_key=True,
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

    language_code = db.Column(
        db.String(5),
        nullable=False,
        index=True,
    )

    name = db.Column(
        db.String(80),
        nullable=False,
    )

    unit = db.relationship(
        "Unit",
        back_populates="translations",
    )
