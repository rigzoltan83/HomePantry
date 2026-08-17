from flask import (
    Flask,
    jsonify,
    url_for,
)

from .config import Config
from .extensions import (
    csrf,
    db,
    login_manager,
    migrate,
)
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

    csrf.init_app(app)

    login_manager.login_view = (
        "auth.login"
    )

    login_manager.login_message = (
        "Please sign in to continue."
    )

    from . import models  # noqa: F401

    from .auth import bp as auth_bp
    from .main import bp as main_bp

    app.register_blueprint(
        auth_bp,
        url_prefix="/auth",
    )

    app.register_blueprint(
        main_bp,
    )

    @login_manager.user_loader
    def load_user(user_id):
        from .models import User

        try:
            numeric_user_id = int(
                user_id
            )
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
            login_url=url_for(
                "auth.login"
            ),
            home_url=url_for(
                "main.index"
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
