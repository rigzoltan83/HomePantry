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

from app.extensions import db
from app.i18n import translate
from app.models import (
    HouseholdMember,
    Ingredient,
    IngredientTranslation,
    IngredientUnit,
    InventoryBatch,
    InventoryMovement,
    Product,
    StorageLocation,
    Unit,
    UnitTranslation,
)

from . import bp
from .forms import (
    InventoryBatchForm,
    StorageLocationForm,
)


LOCATION_TYPES = [
    "room",
    "cabinet",
    "shelf",
    "fridge",
    "freezer",
    "drawer",
    "box",
    "storage",
]


def get_location_type_label(
    location_type,
):
    return translate(
        f"location_type_{location_type}"
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


def build_location_tree(
    locations,
):
    children_by_parent = {}

    for location in locations:
        children_by_parent.setdefault(
            location.parent_id,
            [],
        ).append(
            location
        )

    for children in (
        children_by_parent.values()
    ):
        children.sort(
            key=lambda item: (
                item.sort_order,
                item.name.lower(),
                item.id,
            )
        )

    result = []

    def walk(
        parent_id,
        depth,
    ):
        for location in (
            children_by_parent.get(
                parent_id,
                []
            )
        ):
            result.append(
                (
                    location,
                    depth,
                )
            )

            walk(
                location.id,
                depth + 1,
            )

    walk(
        None,
        0,
    )

    return result


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

    filtered_locations = [
        location
        for location in locations
        if location.id not in excluded_ids
    ]

    tree = build_location_tree(
        filtered_locations
    )

    choices = [
        (
            0,
            translate("no_parent"),
        )
    ]

    for location, depth in tree:
        prefix = (
            "    " * depth
        )

        marker = (
            "↳ "
            if depth > 0
            else ""
        )

        choices.append(
            (
                location.id,
                (
                    f"{prefix}"
                    f"{marker}"
                    f"{location.name}"
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

    active_tree = build_location_tree(
        active_locations
    )

    inactive_tree = build_location_tree(
        inactive_locations
    )

    return render_template(
        "inventory/locations.html",
        active_tree=active_tree,
        inactive_tree=inactive_tree,
        get_location_type_label=(
            get_location_type_label
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

    form.name.label.text = translate(
        "field_name"
    )

    form.location_type.label.text = (
        translate("field_type")
    )

    form.parent_id.label.text = (
        translate("field_parent")
    )

    form.sort_order.label.text = (
        translate("field_sort_order")
    )

    form.submit.label.text = translate(
        "save"
    )

    form.location_type.choices = [
        (
            location_type,
            get_location_type_label(
                location_type
            ),
        )
        for location_type in LOCATION_TYPES
    ]

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
            translate("storage_created"),
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
        page_title=translate(
            "storage_new_title"
        ),
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

    form.name.label.text = translate(
        "field_name"
    )

    form.location_type.label.text = (
        translate("field_type")
    )

    form.parent_id.label.text = (
        translate("field_parent")
    )

    form.sort_order.label.text = (
        translate("field_sort_order")
    )

    form.submit.label.text = translate(
        "save"
    )

    form.location_type.choices = [
        (
            location_type,
            get_location_type_label(
                location_type
            ),
        )
        for location_type in LOCATION_TYPES
    ]

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
            translate("storage_updated"),
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
        page_title=translate(
            "storage_edit_title"
        ),
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
                translate("storage_has_children"),
                "error",
            )

            return redirect(
                url_for(
                    "inventory.locations"
                )
            )

        location.is_active = False

        flash(
            translate("storage_deactivated"),
            "success",
        )

    else:
        if (
            location.parent is not None
            and not location.parent.is_active
        ):
            flash(
                translate("storage_parent_inactive"),
                "error",
            )

            return redirect(
                url_for(
                    "inventory.locations"
                )
            )

        location.is_active = True

        flash(
            translate("storage_reactivated"),
            "success",
        )

    db.session.commit()

    return redirect(
        url_for(
            "inventory.locations"
        )
    )

def get_ingredient_choices():
    ingredients = db.session.scalars(
        select(Ingredient)
        .where(
            Ingredient.is_active.is_(True)
        )
        .order_by(
            Ingredient.canonical_key
        )
    ).all()

    choices = []

    for ingredient in ingredients:
        hu_name = next(
            (
                translation.name
                for translation
                in ingredient.translations
                if translation.language_code
                == "hu"
            ),
            ingredient.canonical_key,
        )

        choices.append(
            (
                ingredient.id,
                hu_name,
            )
        )

    return choices


def get_product_choices(
    household_id,
):
    products = db.session.scalars(
        select(Product)
        .where(
            Product.household_id
            == household_id,
            Product.is_active.is_(
                True
            ),
        )
        .order_by(
            Product.name
        )
    ).all()

    choices = [
        (
            0,
            translate(
                "inventory_bulk_product"
            ),
        )
    ]

    for product in products:
        label = product.name

        if product.brand:
            label = (
                f"{product.brand} — "
                f"{product.name}"
            )

        choices.append(
            (
                product.id,
                label,
            )
        )

    return choices


def get_unit_choices(
    ingredient_id=None,
):
    query = (
        select(Unit)
        .where(
            Unit.is_active.is_(True)
        )
    )

    if ingredient_id:
        query = (
            select(Unit)
            .join(
                IngredientUnit,
                IngredientUnit.unit_id
                == Unit.id,
            )
            .where(
                IngredientUnit.ingredient_id
                == ingredient_id,
                Unit.is_active.is_(True),
            )
            .order_by(
                IngredientUnit.sort_order,
                Unit.sort_order,
                Unit.code,
            )
        )
    else:
        query = query.order_by(
            Unit.sort_order,
            Unit.code,
        )

    units = db.session.scalars(
        query
    ).all()

    choices = []

    for unit in units:
        name = next(
            (
                translation.name
                for translation
                in unit.translations
                if translation.language_code
                == current_user.preferred_language
            ),
            None,
        )

        if name is None:
            name = next(
                (
                    translation.name
                    for translation
                    in unit.translations
                    if translation.language_code
                    == "hu"
                ),
                unit.code,
            )

        choices.append(
            (
                unit.id,
                f"{name} ({unit.symbol})",
            )
        )

    return choices


def get_storage_location_choices(
    household_id,
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
    ).all()

    tree = build_location_tree(
        locations
    )

    choices = []

    for location, depth in tree:
        prefix = (
            "    " * depth
        )

        marker = (
            "↳ "
            if depth > 0
            else ""
        )

        choices.append(
            (
                location.id,
                (
                    f"{prefix}"
                    f"{marker}"
                    f"{location.name}"
                ),
            )
        )

    return choices


@bp.route(
    "/batches/new",
    methods=[
        "GET",
        "POST",
    ],
)
@login_required
def batch_new():
    membership = (
        get_current_membership()
    )

    household_id = (
        membership.household_id
    )

    form = InventoryBatchForm()

    form.ingredient_id.label.text = (
        translate(
            "inventory_field_ingredient"
        )
    )

    form.product_id.label.text = (
        translate(
            "inventory_field_product"
        )
    )

    form.storage_location_id.label.text = (
        translate(
            "inventory_field_location"
        )
    )

    form.quantity.label.text = (
        translate(
            "inventory_field_quantity"
        )
    )

    form.unit_id.label.text = (
        translate(
            "inventory_field_unit"
        )
    )

    form.purchase_date.label.text = (
        translate(
            "inventory_field_purchase_date"
        )
    )

    form.expiration_date.label.text = (
        translate(
            "inventory_field_expiration_date"
        )
    )

    form.note.label.text = translate(
        "inventory_field_note"
    )

    form.submit.label.text = translate(
        "inventory_add_submit"
    )

    form.ingredient_id.choices = (
        get_ingredient_choices()
    )

    form.product_id.choices = (
        get_product_choices(
            household_id
        )
    )

    form.storage_location_id.choices = (
        get_storage_location_choices(
            household_id
        )
    )

    selected_ingredient_id = (
        form.ingredient_id.data
        if form.ingredient_id.data
        else (
            form.ingredient_id.choices[0][0]
            if form.ingredient_id.choices
            else None
        )
    )

    form.unit_id.choices = (
        get_unit_choices(
            selected_ingredient_id
        )
    )

    if form.validate_on_submit():
        ingredient = db.session.get(
            Ingredient,
            form.ingredient_id.data,
        )

        if (
            ingredient is None
            or not ingredient.is_active
        ):
            abort(400)

        product = None

        if form.product_id.data:
            product = db.session.get(
                Product,
                form.product_id.data,
            )

            if (
                product is None
                or product.household_id
                != household_id
                or not product.is_active
            ):
                abort(400)

        location = db.session.get(
            StorageLocation,
            form.storage_location_id.data,
        )

        if (
            location is None
            or location.household_id
            != household_id
            or not location.is_active
        ):
            abort(400)

        unit = db.session.get(
            Unit,
            form.unit_id.data,
        )

        if (
            unit is None
            or not unit.is_active
        ):
            abort(400)

        quantity = form.quantity.data

        batch = InventoryBatch(
            household_id=household_id,
            product=product,
            ingredient=ingredient,
            storage_location=location,
            quantity=quantity,
            unit=unit,
            purchase_date=(
                form.purchase_date.data
            ),
            expiration_date=(
                form.expiration_date.data
            ),
            note=(
                form.note.data.strip()
                if form.note.data
                else None
            ),
            is_active=True,
        )

        db.session.add(
            batch
        )

        db.session.flush()

        movement = InventoryMovement(
            household_id=household_id,
            inventory_batch=batch,
            movement_type=(
                "opening_balance"
            ),
            quantity_delta=quantity,
            unit=unit,
            quantity_before=0,
            quantity_after=quantity,
            created_by_user_id=(
                current_user.id
            ),
            note=(
                "Initial inventory entry"
            ),
        )

        db.session.add(
            movement
        )

        db.session.commit()

        flash(
            translate(
                "inventory_added"
            ),
            "success",
        )

        return redirect(
            url_for(
                "inventory.inventory_list"
            )
        )

    return render_template(
        "inventory/batch_form.html",
        form=form,
    )


@bp.get("/batches")
@login_required
def inventory_list():
    household_id = (
        get_current_household_id()
    )

    batches = db.session.scalars(
        select(InventoryBatch)
        .where(
            InventoryBatch.household_id
            == household_id,
            InventoryBatch.is_active.is_(
                True
            ),
            InventoryBatch.quantity > 0,
        )
        .order_by(
            InventoryBatch.expiration_date
            .asc()
            .nullslast(),
            InventoryBatch.created_at,
        )
    ).all()

    return render_template(
        "inventory/inventory_list.html",
        batches=batches,
        build_location_path=(
            build_location_path
        ),
    )
