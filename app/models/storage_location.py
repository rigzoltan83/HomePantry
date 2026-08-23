import uuid

from sqlalchemy import UniqueConstraint
from sqlalchemy import func

from app.extensions import db


class StorageLocation(db.Model):
    __tablename__ = "storage_locations"

    __table_args__ = (
        UniqueConstraint(
            "household_id",
            "parent_id",
            "name",
            name="uq_storage_location_name",
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

    parent_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "storage_locations.id",
            ondelete="RESTRICT",
        ),
        nullable=True,
        index=True,
    )

    name = db.Column(
        db.String(160),
        nullable=False,
    )

    location_type = db.Column(
        db.String(40),
        nullable=False,
        default="storage",
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

    household = db.relationship(
        "Household",
    )

    parent = db.relationship(
        "StorageLocation",
        remote_side=[id],
        back_populates="children",
    )

    children = db.relationship(
        "StorageLocation",
        back_populates="parent",
    )

    images = db.relationship(
        "StorageLocationImage",
        back_populates="storage_location",
        cascade="all, delete-orphan",
        order_by=(
            "StorageLocationImage.sort_order, "
            "StorageLocationImage.id"
        ),
    )

class StorageLocationImage(db.Model):
    __tablename__ = (
        "storage_location_images"
    )

    __table_args__ = (
        UniqueConstraint(
            "storage_location_id",
            "stored_filename",
            name=(
                "uq_storage_location_image_file"
            ),
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

    storage_location_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "storage_locations.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    original_filename = db.Column(
        db.String(255),
        nullable=True,
    )

    stored_filename = db.Column(
        db.String(255),
        nullable=False,
    )

    sort_order = db.Column(
        db.Integer,
        nullable=False,
        default=100,
    )

    width = db.Column(
        db.Integer,
        nullable=True,
    )

    height = db.Column(
        db.Integer,
        nullable=True,
    )

    file_size = db.Column(
        db.Integer,
        nullable=True,
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    storage_location = db.relationship(
        "StorageLocation",
        back_populates="images",
    )
