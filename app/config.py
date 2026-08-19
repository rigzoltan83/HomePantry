import os


class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "development-only-secret-key",
    )

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    APPLICATION_PREFIX = (
        os.getenv("APPLICATION_PREFIX", "")
        .strip()
        .rstrip("/")
    )

    DEFAULT_TIMEZONE = os.getenv(
        "DEFAULT_TIMEZONE",
        "Europe/Budapest",
    )

    PRODUCT_IMAGE_UPLOAD_DIR = os.getenv(
        "PRODUCT_IMAGE_UPLOAD_DIR",
        (
            "/opt/homepantry/"
            "var/uploads/products"
        ),
    )

    PRODUCT_IMAGE_MAX_SIZE = 1600

    PRODUCT_IMAGE_WEBP_QUALITY = 82

    RECIPE_IMAGE_UPLOAD_DIR = os.getenv(
        "RECIPE_IMAGE_UPLOAD_DIR",
        (
            "/opt/homepantry/"
            "var/uploads/recipes"
        ),
    )

    RECIPE_IMAGE_MAX_SIZE = 1600

    RECIPE_IMAGE_WEBP_QUALITY = 82

    MAX_CONTENT_LENGTH = (
        50 * 1024 * 1024
    )

    OPEN_FOOD_FACTS_USER_AGENT = (
        os.getenv(
            "OPEN_FOOD_FACTS_USER_AGENT",
            (
                "HomePantry/1.0 "
                "(private household inventory)"
            ),
        )
    )
