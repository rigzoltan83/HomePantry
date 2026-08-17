from flask import Flask, jsonify, url_for

from .config import Config
from .extensions import db, login_manager, migrate
from .middleware import PrefixMiddleware


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    if not app.config[
        "SQLALCHEMY_DATABASE_URI"
    ]:
        raise RuntimeError(
            "DATABASE_URL is not configured."
        )

    db.init_app(app)

    migrate.init_app(
        app,
        db,
    )

    login_manager.init_app(app)

    login_manager.login_view = "auth.login"

    # Import models so SQLAlchemy/Alembic can
    # discover every mapped table.
    from . import models  # noqa: F401

    @login_manager.user_loader
    def load_user(user_id):
        from .models import User

        try:
            numeric_user_id = int(user_id)
        except (
            TypeError,
            ValueError,
        ):
            return None

        return db.session.get(
            User,
            numeric_user_id,
        )

    @app.get("/health")
    def health():
        return jsonify(
            status="ok",
            application="HomePantry",
        )

    @app.get("/prefix-test")
    def prefix_test():
        return jsonify(
            health_url=url_for(
                "health"
            ),
            static_url=url_for(
                "static",
                filename="css/app.css",
            ),
        )

    prefix = app.config[
        "APPLICATION_PREFIX"
    ]

    app.wsgi_app = PrefixMiddleware(
        app.wsgi_app,
        prefix=prefix,
    )

    return app
