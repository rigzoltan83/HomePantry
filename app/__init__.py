from flask import Flask, jsonify

from .config import Config
from .extensions import db, migrate
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

    @app.get("/health")
    def health():
        return jsonify(
            status="ok",
            application="HomePantry",
        )

    @app.get("/prefix-test")
    def prefix_test():
        from flask import url_for

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
