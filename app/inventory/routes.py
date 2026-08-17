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
from sqlalchemy import select

from app.extensions import db
from app.models import (
    HouseholdMember,
    StorageLocation,
)

from . import bp
from .forms import StorageLocationForm


LOCATION_TYPE_LABELS = {
    "room": "Room",
    "cabinet": "Cabinet",
    "shelf": "Shelf",
    "fridge": "Fridge",
    "freezer": "Freezer",
    "drawer": "Drawer",
    "box": "Box",
    "storage": "Other storage",
}


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


def get_current_household_id():
    return (
        get_current_membership()
        .household_id
    )


def get_location_or_404(
    public_id,
):
    household_id = (
        get_current_household_id()
    )

    location = db.session.scalar(
        select(StorageLocation)
        .where(
            StorageLocation.public_id
            == public_id,
            StorageLocation.household_id
            == household_id,
        )
    )

    if location is None:
        abort(404)

    return location


def build_location_path(
    location,
):
    parts = []
    current = location

    while current is not None:
        parts.append(
            current.name
        )

        current = (
            current.parent
        )

    return " → ".join(
        reversed(parts)
    )


def get_location_choices(
    household_id,
    excluded_location=None,
):
    locations = db.session.scalars(
        select(StorageLocation)
        .where(
            StorageLocation.household_id
            == household_id,
            StorageLocation.is_active.is_(
                True
            ),
        )
        .order_by(
            StorageLocation.sort_order,
            StorageLocation.name,
        )
    ).all()

    excluded_ids = set()

    if excluded_location is not None:
        def collect_descendants(
            location,
        ):
            excluded_ids.add(
                location.id
            )

            for child in location.children:
                collect_descendants(
                    child
                )

        collect_descendants(
            excluded_location
        )

    choices = [
        (
            0,
            "— No parent —",
        )
    ]

    for location in locations:
        if location.id in excluded_ids:
            continue

        choices.append(
            (
                location.id,
                build_location_path(
                    location
                ),
            )
        )

    return choices


@bp.get("/locations")
@login_required
def locations():
    household_id = (
        get_current_household_id()
    )

    all_locations = db.session.scalars(
        select(StorageLocation)
        .where(
            StorageLocation.household_id
            == household_id
        )
        .order_by(
            StorageLocation.sort_order,
            StorageLocation.name,
        )
    ).all()

    active_locations = [
        location
        for location in all_locations
        if location.is_active
    ]

    inactive_locations = [
        location
        for location in all_locations
        if not location.is_active
    ]

    return render_template(
        "inventory/locations.html",
        active_locations=active_locations,
        inactive_locations=inactive_locations,
        location_type_labels=(
            LOCATION_TYPE_LABELS
        ),
        build_location_path=(
            build_location_path
        ),
    )


@bp.route(
    "/locations/new",
    methods=[
        "GET",
        "POST",
    ],
)
@login_required
def location_new():
    household_id = (
        get_current_household_id()
    )

    form = StorageLocationForm()

    form.parent_id.choices = (
        get_location_choices(
            household_id
        )
    )

    if form.validate_on_submit():
        parent = None

        if form.parent_id.data:
            parent = db.session.get(
                StorageLocation,
                form.parent_id.data,
            )

            if (
                parent is None
                or parent.household_id
                != household_id
                or not parent.is_active
            ):
                abort(400)

        location = StorageLocation(
            household_id=household_id,
            parent=parent,
            name=(
                form.name.data
                .strip()
            ),
            location_type=(
                form.location_type.data
            ),
            sort_order=(
                form.sort_order.data
            ),
            is_active=True,
        )

        db.session.add(
            location
        )

        db.session.commit()

        flash(
            "Storage location created.",
            "success",
        )

        return redirect(
            url_for(
                "inventory.locations"
            )
        )

    return render_template(
        "inventory/location_form.html",
        form=form,
        page_title="New storage location",
    )


@bp.route(
    "/locations/<uuid:public_id>/edit",
    methods=[
        "GET",
        "POST",
    ],
)
@login_required
def location_edit(
    public_id,
):
    location = get_location_or_404(
        public_id
    )

    household_id = (
        location.household_id
    )

    form = StorageLocationForm(
        obj=location
    )

    form.parent_id.choices = (
        get_location_choices(
            household_id,
            excluded_location=location,
        )
    )

    if not form.is_submitted():
        form.parent_id.data = (
            location.parent_id
            or 0
        )

    if form.validate_on_submit():
        parent = None

        if form.parent_id.data:
            parent = db.session.get(
                StorageLocation,
                form.parent_id.data,
            )

            if (
                parent is None
                or parent.household_id
                != household_id
                or not parent.is_active
            ):
                abort(400)

        location.parent = parent

        location.name = (
            form.name.data
            .strip()
        )

        location.location_type = (
            form.location_type.data
        )

        location.sort_order = (
            form.sort_order.data
        )

        db.session.commit()

        flash(
            "Storage location updated.",
            "success",
        )

        return redirect(
            url_for(
                "inventory.locations"
            )
        )

    return render_template(
        "inventory/location_form.html",
        form=form,
        page_title="Edit storage location",
        location=location,
    )


@bp.post(
    "/locations/<uuid:public_id>/toggle"
)
@login_required
def location_toggle(
    public_id,
):
    location = get_location_or_404(
        public_id
    )

    if location.is_active:
        active_children = [
            child
            for child in location.children
            if child.is_active
        ]

        if active_children:
            flash(
                "This location still has "
                "active child locations.",
                "error",
            )

            return redirect(
                url_for(
                    "inventory.locations"
                )
            )

        location.is_active = False

        flash(
            "Storage location deactivated.",
            "success",
        )

    else:
        if (
            location.parent is not None
            and not location.parent.is_active
        ):
            flash(
                "Reactivate the parent "
                "location first.",
                "error",
            )

            return redirect(
                url_for(
                    "inventory.locations"
                )
            )

        location.is_active = True

        flash(
            "Storage location reactivated.",
            "success",
        )

    db.session.commit()

    return redirect(
        url_for(
            "inventory.locations"
        )
    )
