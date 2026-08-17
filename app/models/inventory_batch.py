import uuid

from sqlalchemy import func

from app.extensions import db


class InventoryBatch(db.Model):
    __tablename__ = "inventory_batches"

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

    product_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "products.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    ingredient_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "ingredients.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    storage_location_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "storage_locations.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        index=True,
    )

    quantity = db.Column(
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

    purchase_date = db.Column(
        db.Date,
        nullable=True,
        index=True,
    )

    expiration_date = db.Column(
        db.Date,
        nullable=True,
        index=True,
    )

    opened_at = db.Column(
        db.DateTime(timezone=True),
        nullable=True,
    )

    note = db.Column(
        db.Text,
        nullable=True,
    )

    is_active = db.Column(
        db.Boolean,
        nullable=False,
        default=True,
        index=True,
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

    product = db.relationship(
        "Product",
    )

    ingredient = db.relationship(
        "Ingredient",
    )

    storage_location = db.relationship(
        "StorageLocation",
    )

    unit = db.relationship(
        "Unit",
    )

    movements = db.relationship(
        "InventoryMovement",
        back_populates="inventory_batch",
        cascade="all, delete-orphan",
        order_by="InventoryMovement.created_at",
    )
