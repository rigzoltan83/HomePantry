from flask import (
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import (
    current_user,
    login_user,
    logout_user,
)
from sqlalchemy import (
    or_,
    select,
)
from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)

from app.extensions import db
from app.models import (
    Household,
    HouseholdMember,
    User,
)

from . import bp
from .forms import (
    LoginForm,
    RegisterForm,
)


@bp.route(
    "/register",
    methods=[
        "GET",
        "POST",
    ],
)
def register():
    if current_user.is_authenticated:
        return redirect(
            url_for("main.index")
        )

    form = RegisterForm()

    if form.validate_on_submit():
        email = (
            form.email.data
            .strip()
            .lower()
        )

        username = (
            form.username.data
            .strip()
            .lower()
        )

        existing_user = db.session.scalar(
            select(User).where(
                or_(
                    User.email == email,
                    User.username == username,
                )
            )
        )

        if existing_user is not None:
            flash(
                "An account with this email "
                "or username already exists.",
                "error",
            )

            return render_template(
                "auth/register.html",
                form=form,
            )

        user = User(
            email=email,
            username=username,
            display_name=(
                form.display_name.data
                .strip()
            ),
            preferred_language=(
                form.preferred_language.data
            ),
            password_hash=(
                generate_password_hash(
                    form.password.data
                )
            ),
        )

        household = Household(
            name=(
                form.household_name.data
                .strip()
            ),
            default_language=(
                form.preferred_language.data
            ),
        )

        membership = HouseholdMember(
            user=user,
            household=household,
            role="owner",
        )

        try:
            db.session.add_all(
                [
                    user,
                    household,
                    membership,
                ]
            )

            db.session.commit()

        except Exception:
            db.session.rollback()
            raise

        login_user(user)

        flash(
            "Welcome to HomePantry!",
            "success",
        )

        return redirect(
            url_for("main.index")
        )

    return render_template(
        "auth/register.html",
        form=form,
    )


@bp.route(
    "/login",
    methods=[
        "GET",
        "POST",
    ],
)
def login():
    if current_user.is_authenticated:
        return redirect(
            url_for("main.index")
        )

    form = LoginForm()

    if form.validate_on_submit():
        login_value = (
            form.login.data
            .strip()
            .lower()
        )

        user = db.session.scalar(
            select(User).where(
                or_(
                    User.email == login_value,
                    User.username == login_value,
                )
            )
        )

        if (
            user is None
            or not user.is_active
            or not check_password_hash(
                user.password_hash,
                form.password.data,
            )
        ):
            flash(
                "Invalid email or password.",
                "error",
            )

            return render_template(
                "auth/login.html",
                form=form,
            )

        login_user(user)

        next_url = request.args.get(
            "next"
        )

        if (
            next_url
            and next_url.startswith("/")
            and not next_url.startswith("//")
        ):
            return redirect(next_url)

        return redirect(
            url_for("main.index")
        )

    return render_template(
        "auth/login.html",
        form=form,
    )


@bp.post("/logout")
def logout():
    logout_user()

    return redirect(
        url_for("auth.login")
    )
