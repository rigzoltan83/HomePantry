import uuid

from sqlalchemy import func

from app.extensions import db


class InventoryMovement(db.Model):
    __tablename__ = "inventory_movements"

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

    inventory_batch_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "inventory_batches.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    movement_type = db.Column(
        db.String(30),
        nullable=False,
        index=True,
    )

    quantity_delta = db.Column(
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

    quantity_before = db.Column(
        db.Numeric(
            precision=18,
            scale=6,
        ),
        nullable=False,
    )

    quantity_after = db.Column(
        db.Numeric(
            precision=18,
            scale=6,
        ),
        nullable=False,
    )

    note = db.Column(
        db.Text,
        nullable=True,
    )

    created_by_user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        index=True,
    )

    household = db.relationship(
        "Household",
    )

    inventory_batch = db.relationship(
        "InventoryBatch",
        back_populates="movements",
    )

    unit = db.relationship(
        "Unit",
    )

    created_by_user = db.relationship(
        "User",
    )
