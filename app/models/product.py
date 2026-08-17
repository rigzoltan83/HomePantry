import uuid

from sqlalchemy import UniqueConstraint
from sqlalchemy import func

from app.extensions import db


class Product(db.Model):
    __tablename__ = "products"

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
            ondelete="RESTRICT",
        ),
        nullable=True,
        index=True,
    )

    name = db.Column(
        db.String(255),
        nullable=False,
    )

    brand = db.Column(
        db.String(160),
        nullable=True,
    )

    package_quantity = db.Column(
        db.Numeric(
            precision=18,
            scale=6,
        ),
        nullable=True,
    )

    package_unit_id = db.Column(
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

    household = db.relationship(
        "Household",
    )

    ingredient = db.relationship(
        "Ingredient",
    )

    package_unit = db.relationship(
        "Unit",
    )

    barcodes = db.relationship(
        "ProductBarcode",
        back_populates="product",
        cascade="all, delete-orphan",
    )


class ProductBarcode(db.Model):
    __tablename__ = "product_barcodes"

    __table_args__ = (
        UniqueConstraint(
            "barcode",
            name="uq_product_barcode",
        ),
    )

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "products.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    barcode = db.Column(
        db.String(64),
        nullable=False,
        index=True,
    )

    barcode_type = db.Column(
        db.String(30),
        nullable=True,
    )

    source = db.Column(
        db.String(40),
        nullable=False,
        default="manual",
        index=True,
    )

    is_verified = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    product = db.relationship(
        "Product",
        back_populates="barcodes",
    )
