from flask import (
    abort,
    flash,
    redirect,
    render_template,
    url_for,
)
from flask_login import (
    current_user,
    login_required,
)
from sqlalchemy import (
    or_,
    select,
)

from werkzeug.security import (
    generate_password_hash,
)

from app.extensions import db
from app.i18n import translate
from app.models import (
    HouseholdMember,
    User,
)

from . import bp
from .forms import (
    HouseholdMemberForm,
    NewHouseholdUserForm,
    ProfileForm,
)


def get_current_membership():
    membership = db.session.scalar(
        select(HouseholdMember)
        .where(
            HouseholdMember.user_id
            == current_user.id,
            HouseholdMember.is_active.is_(
                True
            ),
        )
        .order_by(
            HouseholdMember.id
        )
    )

    if membership is None:
        abort(403)

    return membership


def get_admin_membership():
    membership = (
        get_current_membership()
    )

    if membership.role not in {
        "owner",
        "admin",
    }:
        abort(403)

    return membership


def get_member_or_404(
    public_id,
):
    admin_membership = (
        get_admin_membership()
    )

    member = db.session.scalar(
        select(HouseholdMember)
        .join(
            User,
            User.id
            == HouseholdMember.user_id,
        )
        .where(
            User.public_id
            == public_id,
            HouseholdMember.household_id
            == admin_membership.household_id,
        )
    )

    if member is None:
        abort(404)

    return (
        admin_membership,
        member,
    )


def user_identity_conflict(
    user,
    username,
    email,
):
    return db.session.scalar(
        select(User).where(
            User.id != user.id,
            or_(
                User.username
                == username,
                User.email
                == email,
            ),
        )
    )


def configure_profile_labels(
    form,
):
    form.display_name.label.text = (
        translate(
            "profile_display_name"
        )
    )

    form.username.label.text = (
        translate(
            "profile_username"
        )
    )

    form.email.label.text = (
        translate(
            "profile_email"
        )
    )

    form.preferred_language.label.text = (
        translate(
            "profile_language"
        )
    )

    form.measurement_system.label.text = (
        translate(
            "profile_measurement_system"
        )
    )

    form.submit.label.text = (
        translate("save")
    )


@bp.route(
    "/profile",
    methods=[
        "GET",
        "POST",
    ],
)
@login_required
def profile():
    form = ProfileForm(
        obj=current_user
    )

    configure_profile_labels(
        form
    )

    if form.validate_on_submit():
        username = (
            form.username.data
            .strip()
            .lower()
        )

        email = (
            form.email.data
            .strip()
            .lower()
        )

        conflict = (
            user_identity_conflict(
                current_user,
                username,
                email,
            )
        )

        if conflict is not None:
            flash(
                translate(
                    "profile_identity_exists"
                ),
                "error",
            )

            return render_template(
                "admin/profile.html",
                form=form,
            )

        current_user.display_name = (
            form.display_name.data
            .strip()
        )

        current_user.username = (
            username
        )

        current_user.email = email

        current_user.preferred_language = (
            form.preferred_language.data
        )

        current_user.measurement_system = (
            form.measurement_system.data
        )

        db.session.commit()

        flash(
            translate(
                "profile_updated"
            ),
            "success",
        )

        return redirect(
            url_for(
                "admin.profile"
            )
        )

    return render_template(
        "admin/profile.html",
        form=form,
    )


@bp.get("/users")
@login_required
def users():
    membership = (
        get_admin_membership()
    )

    members = db.session.scalars(
        select(HouseholdMember)
        .where(
            HouseholdMember.household_id
            == membership.household_id
        )
        .join(
            User,
            User.id
            == HouseholdMember.user_id,
        )
        .order_by(
            User.display_name,
            User.username,
        )
    ).all()

    return render_template(
        "admin/users.html",
        members=members,
        current_membership=membership,
    )


@bp.route(
    "/users/new",
    methods=[
        "GET",
        "POST",
    ],
)
@login_required
def user_new():
    admin_membership = (
        get_admin_membership()
    )

    form = NewHouseholdUserForm()

    form.display_name.label.text = (
        translate(
            "profile_display_name"
        )
    )

    form.username.label.text = (
        translate(
            "profile_username"
        )
    )

    form.email.label.text = (
        translate(
            "profile_email"
        )
    )

    form.password.label.text = (
        translate(
            "admin_password"
        )
    )

    form.preferred_language.label.text = (
        translate(
            "profile_language"
        )
    )

    form.measurement_system.label.text = (
        translate(
            "profile_measurement_system"
        )
    )

    form.role.label.text = translate(
        "admin_role"
    )

    form.submit.label.text = translate(
        "admin_add_user"
    )

    if form.validate_on_submit():
        username = (
            form.username.data
            .strip()
            .lower()
        )

        email = (
            form.email.data
            .strip()
            .lower()
        )

        existing_user = db.session.scalar(
            select(User).where(
                or_(
                    User.username
                    == username,
                    User.email
                    == email,
                )
            )
        )

        if existing_user is not None:
            flash(
                translate(
                    "profile_identity_exists"
                ),
                "error",
            )

            return render_template(
                "admin/user_new.html",
                form=form,
            )

        user = User(
            display_name=(
                form.display_name.data
                .strip()
            ),
            username=username,
            email=email,
            password_hash=(
                generate_password_hash(
                    form.password.data
                )
            ),
            preferred_language=(
                form.preferred_language.data
            ),
            measurement_system=(
                form.measurement_system.data
            ),
        )

        membership = HouseholdMember(
            household_id=(
                admin_membership
                .household_id
            ),
            user=user,
            role=form.role.data,
            is_active=True,
        )

        db.session.add_all(
            [
                user,
                membership,
            ]
        )

        db.session.commit()

        flash(
            translate(
                "admin_user_created"
            ),
            "success",
        )

        return redirect(
            url_for(
                "admin.users"
            )
        )

    return render_template(
        "admin/user_new.html",
        form=form,
    )


@bp.route(
    "/users/<uuid:public_id>/edit",
    methods=[
        "GET",
        "POST",
    ],
)
@login_required
def user_edit(
    public_id,
):
    (
        admin_membership,
        membership,
    ) = get_member_or_404(
        public_id
    )

    user = membership.user

    if (
        admin_membership.role
        == "admin"
        and membership.role
        == "owner"
    ):
        abort(403)

    form = HouseholdMemberForm(
        obj=user
    )

    configure_profile_labels(
        form
    )

    form.role.label.text = translate(
        "admin_role"
    )

    form.is_active.label.text = (
        translate(
            "admin_active"
        )
    )

    if not form.is_submitted():
        form.role.data = (
            membership.role
        )

        form.is_active.data = (
            membership.is_active
        )

    if form.validate_on_submit():
        username = (
            form.username.data
            .strip()
            .lower()
        )

        email = (
            form.email.data
            .strip()
            .lower()
        )

        conflict = (
            user_identity_conflict(
                user,
                username,
                email,
            )
        )

        if conflict is not None:
            flash(
                translate(
                    "profile_identity_exists"
                ),
                "error",
            )

            return render_template(
                "admin/user_form.html",
                form=form,
                member=membership,
            )

        # An admin cannot promote anyone to owner.
        if (
            admin_membership.role
            == "admin"
            and form.role.data
            == "owner"
        ):
            abort(403)

        # Do not allow the current owner to accidentally
        # remove their own owner role or membership.
        if (
            membership.user_id
            == current_user.id
            and membership.role
            == "owner"
        ):
            form.role.data = "owner"
            form.is_active.data = True

        user.display_name = (
            form.display_name.data
            .strip()
        )

        user.username = username
        user.email = email

        user.preferred_language = (
            form.preferred_language.data
        )

        user.measurement_system = (
            form.measurement_system.data
        )

        membership.role = (
            form.role.data
        )

        membership.is_active = (
            form.is_active.data
        )

        db.session.commit()

        flash(
            translate(
                "admin_user_updated"
            ),
            "success",
        )

        return redirect(
            url_for(
                "admin.users"
            )
        )

    return render_template(
        "admin/user_form.html",
        form=form,
        member=membership,
    )
