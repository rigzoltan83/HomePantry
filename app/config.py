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

