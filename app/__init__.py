from flask import (
    Flask,
    jsonify,
    url_for,
)

from werkzeug.middleware.proxy_fix import ProxyFix

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
    from .inventory import bp as inventory_bp
    from .main import bp as main_bp

    app.register_blueprint(
        auth_bp,
        url_prefix="/auth",
    )

    app.register_blueprint(
        main_bp,
    )

    app.register_blueprint(
        inventory_bp,
        url_prefix="/inventory",
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
        from flask import request

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
            path=request.path,
            script_name=request.environ.get(
                "SCRIPT_NAME",
                "",
            ),
            forwarded_prefix=request.headers.get(
                "X-Forwarded-Prefix"
            ),
            forwarded_host=request.headers.get(
                "X-Forwarded-Host"
            ),
            forwarded_proto=request.headers.get(
                "X-Forwarded-Proto"
            ),
            host=request.headers.get(
                "Host"
            ),
        )

    prefix = app.config[
        "APPLICATION_PREFIX"
    ]

    app.wsgi_app = ProxyFix(
        app.wsgi_app,
        x_proto=1,
        x_host=1,
    )

    app.wsgi_app = PrefixMiddleware(
        app.wsgi_app,
        prefix=prefix,
    )

    return app
