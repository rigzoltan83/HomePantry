import uuid
from pathlib import Path

from flask import current_app
from PIL import (
    Image,
    ImageOps,
    UnidentifiedImageError,
)

from app.extensions import db
from app.models import (
    StorageLocationImage,
)


ALLOWED_IMAGE_FORMATS = {
    "JPEG",
    "PNG",
    "WEBP",
}


def get_storage_location_image_directory(
    storage_location,
):
    upload_root = Path(
        current_app.config[
            "STORAGE_LOCATION_IMAGE_UPLOAD_DIR"
        ]
    )

    return (
        upload_root
        / str(storage_location.public_id)
    )


def save_storage_location_image(
    storage_location,
    file_storage,
):
    if (
        file_storage is None
        or not file_storage.filename
    ):
        return None

    try:
        image = Image.open(
            file_storage.stream
        )

        image.load()

    except (
        UnidentifiedImageError,
        OSError,
    ) as exc:
        raise ValueError(
            "Invalid image file."
        ) from exc

    if image.format not in (
        ALLOWED_IMAGE_FORMATS
    ):
        raise ValueError(
            "Unsupported image format."
        )

    image = ImageOps.exif_transpose(
        image
    )

    max_size = int(
        current_app.config[
            "STORAGE_LOCATION_IMAGE_MAX_SIZE"
        ]
    )

    image.thumbnail(
        (
            max_size,
            max_size,
        ),
        Image.Resampling.LANCZOS,
    )

    if image.mode in {
        "RGBA",
        "LA",
    }:
        image = image.convert(
            "RGBA"
        )
    else:
        image = image.convert(
            "RGB"
        )

    storage_directory = (
        get_storage_location_image_directory(
            storage_location
        )
    )

    storage_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    stored_filename = (
        f"{uuid.uuid4().hex}.webp"
    )

    destination = (
        storage_directory
        / stored_filename
    )

    image.save(
        destination,
        format="WEBP",
        quality=int(
            current_app.config[
                "STORAGE_LOCATION_IMAGE_WEBP_QUALITY"
            ]
        ),
        method=6,
    )

    existing_image_count = len(
        storage_location.images
    )

    storage_image = (
        StorageLocationImage(
            storage_location=(
                storage_location
            ),
            original_filename=(
                file_storage.filename[:255]
            ),
            stored_filename=(
                stored_filename
            ),
            sort_order=(
                (
                    existing_image_count
                    + 1
                )
                * 10
            ),
            width=image.width,
            height=image.height,
            file_size=(
                destination.stat().st_size
            ),
        )
    )

    db.session.add(
        storage_image
    )

    return storage_image


def delete_storage_location_image_file(
    storage_image,
):
    storage_directory = (
        get_storage_location_image_directory(
            storage_image.storage_location
        )
    )

    image_path = (
        storage_directory
        / storage_image.stored_filename
    )

    if image_path.exists():
        image_path.unlink()

    try:
        storage_directory.rmdir()
    except OSError:
        pass
