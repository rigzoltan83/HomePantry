import uuid
from pathlib import Path

from flask import current_app
from PIL import (
    Image,
    ImageOps,
    UnidentifiedImageError,
)

from app.extensions import db
from app.models import RecipeImage


ALLOWED_IMAGE_FORMATS = {
    "JPEG",
    "PNG",
    "WEBP",
}


def get_recipe_image_directory(
    recipe,
):
    upload_root = Path(
        current_app.config[
            "RECIPE_IMAGE_UPLOAD_DIR"
        ]
    )

    return (
        upload_root
        / str(recipe.public_id)
    )


def save_recipe_image(
    recipe,
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
            "RECIPE_IMAGE_MAX_SIZE"
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

    recipe_directory = (
        get_recipe_image_directory(
            recipe
        )
    )

    recipe_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    stored_filename = (
        f"{uuid.uuid4().hex}.webp"
    )

    destination = (
        recipe_directory
        / stored_filename
    )

    image.save(
        destination,
        format="WEBP",
        quality=int(
            current_app.config[
                "RECIPE_IMAGE_WEBP_QUALITY"
            ]
        ),
        method=6,
    )

    existing_image_count = len(
        recipe.images
    )

    recipe_image = RecipeImage(
        recipe=recipe,
        original_filename=(
            file_storage.filename[
                :255
            ]
        ),
        stored_filename=(
            stored_filename
        ),
        is_cover=(
            existing_image_count == 0
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

    db.session.add(
        recipe_image
    )

    return recipe_image


def delete_recipe_image_file(
    recipe_image,
):
    recipe_directory = (
        get_recipe_image_directory(
            recipe_image.recipe
        )
    )

    image_path = (
        recipe_directory
        / recipe_image.stored_filename
    )

    if image_path.exists():
        image_path.unlink()

    try:
        recipe_directory.rmdir()
    except OSError:
        pass
