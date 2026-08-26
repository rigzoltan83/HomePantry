import os


class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "development-only-secret-key",
    )

    SESSION_COOKIE_NAME = (
        "homepantry_session"
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

    THEMEALDB_API_KEY = os.getenv(
        "THEMEALDB_API_KEY",
        "1",
    )

    THEMEALDB_API_BASE_URL = (
        "https://www.themealdb.com/"
        "api/json/v1"
    )

    ONLINE_RECIPE_TIMEOUT = 15

    RECIPE_TRANSLATION_API_URL = (
        os.getenv(
            "RECIPE_TRANSLATION_API_URL",
            "http://127.0.0.1:5000",
        )
        .strip()
        .rstrip("/")
    )

    RECIPE_TRANSLATION_TIMEOUT = 30

    RECIPE_TRANSLATION_MAX_CHARS = 15000

    ONLINE_RECIPE_IMAGE_MAX_BYTES = (
        10 * 1024 * 1024
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

    STORAGE_LOCATION_IMAGE_UPLOAD_DIR = (
        os.getenv(
            "STORAGE_LOCATION_IMAGE_UPLOAD_DIR",
            (
                "/opt/homepantry/"
                "var/uploads/storage-locations"
            ),
        )
    )

    STORAGE_LOCATION_IMAGE_MAX_SIZE = (
        1600
    )

    STORAGE_LOCATION_IMAGE_WEBP_QUALITY = (
        82
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
