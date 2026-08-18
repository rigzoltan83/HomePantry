import os
from datetime import (
    date,
    timedelta,
)
from decimal import Decimal
from flask import (
    abort,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
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
    ProductBarcode,
    ProductImage,
    StorageLocation,
    StockRule,
    Unit,
    UnitTranslation,
)

from . import bp
from .forms import (
    BatchAdjustmentForm,
    BatchQuantityActionForm,
    BatchTransferForm,
    InventoryBatchForm,
    ProductForm,
    StockRuleForm,
    StorageLocationForm,
)

from .product_images import (
    delete_product_image_file,
    save_product_image,
)

EXPIRING_SOON_DAYS = 3
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
            Ingredient.is_active.is_(
                True
            )
        )
        .order_by(
            Ingredient.canonical_key
        )
    ).all()

    choices = [
        (
            0,
            translate(
                "ingredient_select_placeholder"
            ),
        )
    ]

    for ingredient in ingredients:
        name = next(
            (
                translation.name
                for translation
                in ingredient.translations
                if translation.language_code
                == current_user
                .preferred_language
            ),
            None,
        )

        if name is None:
            name = next(
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
                name,
            )
        )

    return choices


def get_product_or_404(
    public_id,
):
    household_id = (
        get_current_household_id()
    )

    product = db.session.scalar(
        select(Product)
        .where(
            Product.public_id
            == public_id,
            Product.household_id
            == household_id,
        )
    )

    if product is None:
        abort(404)

    return product


def get_batch_or_404(
    public_id,
):
    household_id = (
        get_current_household_id()
    )

    batch = db.session.scalar(
        select(InventoryBatch)
        .where(
            InventoryBatch.public_id
            == public_id,
            InventoryBatch.household_id
            == household_id,
        )
    )

    if batch is None:
        abort(404)

    return batch


def get_stock_rule_or_404(
    public_id,
):
    household_id = (
        get_current_household_id()
    )

    rule = db.session.scalar(
        select(StockRule)
        .where(
            StockRule.public_id
            == public_id,
            StockRule.household_id
            == household_id,
        )
    )

    if rule is None:
        abort(404)

    return rule


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


def get_batch_unit_choices(
    batch,
):
    return get_unit_choices(
        batch.ingredient_id
    )


def configure_product_form(
    form,
    household_id,
):
    form.ingredient_id.label.text = (
        translate(
            "product_field_ingredient"
        )
    )

    form.name.label.text = translate(
        "product_field_name"
    )

    form.brand.label.text = translate(
        "product_field_brand"
    )

    form.package_quantity.label.text = (
        translate(
            "product_field_package_quantity"
        )
    )

    form.package_unit_id.label.text = (
        translate(
            "product_field_package_unit"
        )
    )

    form.barcode.label.text = translate(
        "product_field_barcode"
    )

    form.barcode_type.label.text = (
        translate(
            "product_field_barcode_type"
        )
    )

    form.images.label.text = (
        translate(
            "product_field_images"
        )
    )

    form.submit.label.text = translate(
        "save"
    )

    form.ingredient_id.choices = (
        get_ingredient_choices()
    )

    selected_ingredient_id = (
        form.ingredient_id.data
        if form.ingredient_id.data
        else None
    )

    unit_choices = []

    if selected_ingredient_id:
        unit_choices = get_unit_choices(
            selected_ingredient_id
        )

    form.package_unit_id.choices = [
        (
            0,
            translate(
                "product_no_package_unit"
            ),
        ),
        *unit_choices,
    ]

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


@bp.get("/products")
@login_required
def products():
    household_id = (
        get_current_household_id()
    )

    products = db.session.scalars(
        select(Product)
        .where(
            Product.household_id
            == household_id
        )
        .order_by(
            Product.is_active.desc(),
            Product.name,
        )
    ).all()

    return render_template(
        "inventory/products.html",
        products=products,
    )


@bp.route(
    "/products/new",
    methods=[
        "GET",
        "POST",
    ],
)
@login_required
def product_new():
    household_id = (
        get_current_household_id()
    )

    form = ProductForm()

    requested_ingredient_id = (
        request.args.get(
            "ingredient_id",
            type=int,
        )
    )

    if (
        not form.is_submitted()
        and requested_ingredient_id
    ):
        ingredient = db.session.get(
            Ingredient,
            requested_ingredient_id,
        )

        if (
            ingredient is not None
            and ingredient.is_active
        ):
            form.ingredient_id.data = (
                ingredient.id
            )

    configure_product_form(
        form,
        household_id,
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

        package_unit = None

        if form.package_unit_id.data:
            package_unit = db.session.get(
                Unit,
                form.package_unit_id.data,
            )

            if package_unit is None:
                abort(400)

            allowed = db.session.scalar(
                select(IngredientUnit)
                .where(
                    IngredientUnit.ingredient_id
                    == ingredient.id,
                    IngredientUnit.unit_id
                    == package_unit.id,
                )
            )

            if allowed is None:
                abort(400)

        barcode_value = (
            form.barcode.data.strip()
            if form.barcode.data
            else None
        )

        if barcode_value:
            existing_barcode = (
                db.session.scalar(
                    select(ProductBarcode)
                    .where(
                        ProductBarcode.barcode
                        == barcode_value
                    )
                )
            )

            if existing_barcode is not None:
                flash(
                    translate(
                        "product_barcode_exists"
                    ),
                    "error",
                )

                return render_template(
                    "inventory/product_form.html",
                    form=form,
                    page_title=translate(
                        "product_new_title"
                    ),
                    product=None,
                )

        product = Product(
            household_id=household_id,
            ingredient=ingredient,
            name=(
                form.name.data
                .strip()
            ),
            brand=(
                form.brand.data.strip()
                if form.brand.data
                else None
            ),
            package_quantity=(
                form.package_quantity.data
            ),
            package_unit=package_unit,
            is_active=True,
        )

        db.session.add(product)
        db.session.flush()

        saved_images = []

        try:
            for image_file in (
                form.images.data
                or []
            ):
                if (
                    image_file
                    and image_file.filename
                ):
                    saved_image = (
                        save_product_image(
                            product,
                            image_file,
                        )
                    )

                    if saved_image is not None:
                        saved_images.append(
                            saved_image
                        )

        except ValueError:
            for saved_image in (
                saved_images
            ):
                delete_product_image_file(
                    saved_image
                )

            db.session.rollback()

            flash(
                translate(
                    "product_image_invalid"
                ),
                "error",
            )

            return render_template(
                "inventory/product_form.html",
                form=form,
                page_title=translate(
                    "product_new_title"
                ),
                product=None,
            )

        if barcode_value:
            barcode = ProductBarcode(
                product=product,
                barcode=barcode_value,
                barcode_type=(
                    form.barcode_type.data
                    or None
                ),
                source="manual",
                is_verified=True,
            )

            db.session.add(barcode)

        db.session.commit()

        flash(
            translate(
                "product_created"
            ),
            "success",
        )

        return redirect(
            url_for(
                "inventory.products"
            )
        )

    return render_template(
        "inventory/product_form.html",
        form=form,
        page_title=translate(
            "product_new_title"
        ),
        product=None,
    )


@bp.route(
    "/products/<uuid:public_id>/edit",
    methods=[
        "GET",
        "POST",
    ],
)
@login_required
def product_edit(
    public_id,
):
    product = get_product_or_404(
        public_id
    )

    form = ProductForm(
        obj=product
    )

    if not form.is_submitted():
        form.ingredient_id.data = (
            product.ingredient_id
        )

        form.package_unit_id.data = (
            product.package_unit_id
            or 0
        )

        primary_barcode = (
            product.barcodes[0]
            if product.barcodes
            else None
        )

        if primary_barcode:
            form.barcode.data = (
                primary_barcode.barcode
            )

            form.barcode_type.data = (
                primary_barcode.barcode_type
                or ""
            )

    configure_product_form(
        form,
        product.household_id,
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

        package_unit = None

        if form.package_unit_id.data:
            package_unit = db.session.get(
                Unit,
                form.package_unit_id.data,
            )

            if package_unit is None:
                abort(400)

            allowed = db.session.scalar(
                select(IngredientUnit)
                .where(
                    IngredientUnit.ingredient_id
                    == ingredient.id,
                    IngredientUnit.unit_id
                    == package_unit.id,
                )
            )

            if allowed is None:
                abort(400)

        barcode_value = (
            form.barcode.data.strip()
            if form.barcode.data
            else None
        )

        existing_barcode = None

        if barcode_value:
            existing_barcode = (
                db.session.scalar(
                    select(ProductBarcode)
                    .where(
                        ProductBarcode.barcode
                        == barcode_value
                    )
                )
            )

            if (
                existing_barcode is not None
                and existing_barcode.product_id
                != product.id
            ):
                flash(
                    translate(
                        "product_barcode_exists"
                    ),
                    "error",
                )

                return render_template(
                    "inventory/product_form.html",
                    form=form,
                    page_title=translate(
                        "product_edit_title"
                    ),
                    product=product,
                )

        product.ingredient = ingredient

        product.name = (
            form.name.data.strip()
        )

        product.brand = (
            form.brand.data.strip()
            if form.brand.data
            else None
        )

        product.package_quantity = (
            form.package_quantity.data
        )

        product.package_unit = (
            package_unit
        )

        if product.barcodes:
            barcode = product.barcodes[0]

            if barcode_value:
                barcode.barcode = (
                    barcode_value
                )

                barcode.barcode_type = (
                    form.barcode_type.data
                    or None
                )

                barcode.is_verified = True

            else:
                db.session.delete(
                    barcode
                )

        elif barcode_value:
            db.session.add(
                ProductBarcode(
                    product=product,
                    barcode=barcode_value,
                    barcode_type=(
                        form.barcode_type.data
                        or None
                    ),
                    source="manual",
                    is_verified=True,
                )
            )

        saved_images = []

        try:
            for image_file in (
                form.images.data
                or []
            ):
                if (
                    image_file
                    and image_file.filename
                ):
                    saved_image = (
                        save_product_image(
                            product,
                            image_file,
                        )
                    )

                    if saved_image is not None:
                        saved_images.append(
                            saved_image
                        )

        except ValueError:
            for saved_image in (
                saved_images
            ):
                delete_product_image_file(
                    saved_image
                )

            db.session.rollback()

            flash(
                translate(
                    "product_image_invalid"
                ),
                "error",
            )

            return render_template(
                "inventory/product_form.html",
                form=form,
                page_title=translate(
                    "product_edit_title"
                ),
                product=product,
            )

        db.session.commit()

        flash(
            translate(
                "product_updated"
            ),
            "success",
        )

        return redirect(
            url_for(
                "inventory.products"
            )
        )

    return render_template(
        "inventory/product_form.html",
        form=form,
        page_title=translate(
            "product_edit_title"
        ),
        product=product,
    )


@bp.get(
    "/product-images/<uuid:public_id>"
)
@login_required
def product_image(
    public_id,
):
    household_id = (
        get_current_household_id()
    )

    image = db.session.scalar(
        select(ProductImage)
        .join(
            Product,
            Product.id
            == ProductImage.product_id,
        )
        .where(
            ProductImage.public_id
            == public_id,
            Product.household_id
            == household_id,
        )
    )

    if image is None:
        abort(404)

    product_directory = (
        current_app.config[
            "PRODUCT_IMAGE_UPLOAD_DIR"
        ]
    )

    directory = os.path.join(
        product_directory,
        str(image.product.public_id),
    )

    return send_from_directory(
        directory,
        image.stored_filename,
        mimetype="image/webp",
        max_age=86400,
    )


@bp.post(
    "/products/<uuid:product_public_id>/images/"
    "<uuid:image_public_id>/cover"
)
@login_required
def product_image_cover(
    product_public_id,
    image_public_id,
):
    product = get_product_or_404(
        product_public_id
    )

    image = db.session.scalar(
        select(ProductImage)
        .where(
            ProductImage.public_id
            == image_public_id,
            ProductImage.product_id
            == product.id,
        )
    )

    if image is None:
        abort(404)

    for product_image in (
        product.images
    ):
        product_image.is_cover = (
            product_image.id
            == image.id
        )

    db.session.commit()

    flash(
        translate(
            "product_image_cover_updated"
        ),
        "success",
    )

    return redirect(
        url_for(
            "inventory.product_edit",
            public_id=(
                product.public_id
            ),
        )
    )


@bp.post(
    "/products/<uuid:product_public_id>/images/"
    "<uuid:image_public_id>/delete"
)
@login_required
def product_image_delete(
    product_public_id,
    image_public_id,
):
    product = get_product_or_404(
        product_public_id
    )

    image = db.session.scalar(
        select(ProductImage)
        .where(
            ProductImage.public_id
            == image_public_id,
            ProductImage.product_id
            == product.id,
        )
    )

    if image is None:
        abort(404)

    was_cover = image.is_cover

    delete_product_image_file(
        image
    )

    db.session.delete(
        image
    )

    db.session.flush()

    if was_cover:
        next_image = db.session.scalar(
            select(ProductImage)
            .where(
                ProductImage.product_id
                == product.id,
                ProductImage.id
                != image.id,
            )
            .order_by(
                ProductImage.sort_order,
                ProductImage.id,
            )
            .limit(1)
        )

        if next_image is not None:
            next_image.is_cover = True

    db.session.commit()

    flash(
        translate(
            "product_image_deleted"
        ),
        "success",
    )

    return redirect(
        url_for(
            "inventory.product_edit",
            public_id=(
                product.public_id
            ),
        )
    )


@bp.post(
    "/products/<uuid:public_id>/toggle"
)
@login_required
def product_toggle(
    public_id,
):
    product = get_product_or_404(
        public_id
    )

    product.is_active = (
        not product.is_active
    )

    db.session.commit()

    flash(
        translate(
            (
                "product_reactivated"
                if product.is_active
                else "product_deactivated"
            )
        ),
        "success",
    )

    return redirect(
        url_for(
            "inventory.products"
        )
    )


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

    if not form.is_submitted():
        form.purchase_date.data = (
            date.today()
        )

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
        else None
    )

    unit_choices = []

    if selected_ingredient_id:
        unit_choices = get_unit_choices(
            selected_ingredient_id
        )

    form.unit_id.choices = (
        unit_choices
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

        barcode_value = (
            form.barcode.data.strip()
            if form.barcode.data
            else None
        )

        if barcode_value:
            barcode_record = db.session.scalar(
                select(ProductBarcode)
                .join(
                    Product,
                    Product.id
                    == ProductBarcode.product_id,
                )
                .where(
                    ProductBarcode.barcode
                    == barcode_value,
                    Product.household_id
                    == household_id,
                )
            )

            if barcode_record is not None:
                product = (
                    barcode_record.product
                )

        if (
            product is None
            and form.product_id.data
        ):
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

        created_new_product = False

        if (
            barcode_value
            and product is None
        ):
            product_name = (
                form.new_product_name.data.strip()
                if form.new_product_name.data
                else ""
            )

            if not product_name:
                form.new_product_name.errors.append(
                    translate(
                        "barcode_new_product_name_required"
                    )
                )

                return render_template(
                    "inventory/batch_form.html",
                    form=form,
                )

            product = Product(
                household_id=household_id,
                ingredient=ingredient,
                name=product_name,
                brand=(
                    form.new_product_brand.data.strip()
                    if form.new_product_brand.data
                    else None
                ),
                package_quantity=(
                    form.quantity.data
                ),
                package_unit=unit,
                is_active=True,
            )

            db.session.add(
                product
            )

            db.session.flush()

            product_barcode = ProductBarcode(
                product=product,
                barcode=barcode_value,
                barcode_type=None,
                source="manual",
                is_verified=True,
            )

            db.session.add(
                product_barcode
            )

            created_new_product = True

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
                (
                    "barcode_product_created_with_stock"
                    if created_new_product
                    else "inventory_added"
                )
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


def get_ingredient_display_name(
    ingredient,
):
    preferred_language = (
        current_user.preferred_language
        or "hu"
    )

    name = next(
        (
            translation.name
            for translation
            in ingredient.translations
            if translation.language_code
            == preferred_language
        ),
        None,
    )

    if name is None:
        name = next(
            (
                translation.name
                for translation
                in ingredient.translations
                if translation.language_code
                == "hu"
            ),
            None,
        )

    return (
        name
        or ingredient.canonical_key
    )


def format_decimal_quantity(
    value,
):
    value = Decimal(value)

    normalized = format(
        value.normalize(),
        "f",
    )

    if "." in normalized:
        normalized = normalized.rstrip(
            "0"
        ).rstrip(".")

    return normalized


def convert_quantity(
    quantity,
    source_unit,
    target_unit,
):
    if (
        source_unit.dimension
        != target_unit.dimension
    ):
        raise ValueError(
            "Unit dimensions do not match."
        )

    base_quantity = (
        Decimal(quantity)
        * Decimal(
            source_unit.factor_to_base
        )
    )

    return (
        base_quantity
        / Decimal(
            target_unit.factor_to_base
        )
    )


def build_inventory_display_total(
    dimension,
    base_quantity,
    ingredient,
):
    measurement_system = (
        current_user.measurement_system
        or "metric"
    )

    unit_codes = []

    if measurement_system == "metric":
        if dimension == "mass":
            if base_quantity >= Decimal("1000"):
                unit_codes = ["kg", "g"]
            else:
                unit_codes = ["g", "kg"]

        elif dimension == "volume":
            if base_quantity >= Decimal("1000"):
                unit_codes = ["l", "ml"]
            else:
                unit_codes = ["ml", "l"]

        elif dimension == "count":
            unit_codes = ["pc"]

    elif measurement_system == "us_customary":
        if dimension == "mass":
            unit_codes = [
                "lb",
                "oz",
            ]

        elif dimension == "volume":
            unit_codes = [
                "gallon_us",
                "quart_us",
                "pint_us",
                "cup_us",
                "fl_oz_us",
            ]

        elif dimension == "count":
            unit_codes = ["pc"]

    elif measurement_system == "imperial":
        if dimension == "mass":
            unit_codes = [
                "lb",
                "oz",
            ]

        elif dimension == "volume":
            unit_codes = [
                "gallon_imp",
                "quart_imp",
                "pint_imp",
                "fl_oz_imp",
            ]

        elif dimension == "count":
            unit_codes = ["pc"]

    display_unit = None

    for code in unit_codes:
        candidate = db.session.scalar(
            select(Unit)
            .where(
                Unit.code == code,
                Unit.is_active.is_(True),
            )
        )

        if (
            candidate is not None
            and candidate.dimension
            == dimension
        ):
            display_unit = candidate
            break

    if (
        display_unit is None
        and ingredient.default_unit
        is not None
        and ingredient.default_unit.dimension
        == dimension
    ):
        display_unit = (
            ingredient.default_unit
        )

    if display_unit is None:
        display_unit = db.session.scalar(
            select(Unit)
            .where(
                Unit.dimension == dimension,
                Unit.factor_to_base
                == Decimal("1"),
                Unit.is_active.is_(True),
            )
            .order_by(
                Unit.sort_order,
                Unit.id,
            )
        )

    if display_unit is None:
        return None

    display_quantity = (
        Decimal(base_quantity)
        / Decimal(
            display_unit.factor_to_base
        )
    )

    if dimension in {
        "mass",
        "volume",
    }:
        display_quantity = (
            display_quantity.quantize(
                Decimal("0.001")
            )
        )

    return {
        "dimension": dimension,
        "quantity": (
            format_decimal_quantity(
                display_quantity
            )
        ),
        "symbol": display_unit.symbol,
    }


@bp.route(
    "/batches/<uuid:public_id>/<action>",
    methods=[
        "GET",
        "POST",
    ],
)
@login_required
def batch_quantity_action(
    public_id,
    action,
):
    if action not in {
        "consume",
        "discard",
    }:
        abort(404)

    batch = get_batch_or_404(
        public_id
    )

    if (
        not batch.is_active
        or batch.quantity <= 0
    ):
        abort(400)

    form = BatchQuantityActionForm()

    form.quantity.label.text = (
        translate(
            "movement_quantity"
        )
    )

    form.note.label.text = (
        translate(
            "inventory_field_note"
        )
    )

    form.submit.label.text = (
        translate(
            (
                "movement_consume"
                if action == "consume"
                else "movement_discard"
            )
        )
    )

    if form.validate_on_submit():
        quantity_in_batch_unit = Decimal(
            form.quantity.data
        )

        if (
            quantity_in_batch_unit
            > Decimal(
                batch.quantity
            )
        ):
            form.quantity.errors.append(
                translate(
                    "movement_too_much"
                )
            )

            return render_template(
                "inventory/batch_action.html",
                form=form,
                batch=batch,
                action=action,
                build_location_path=(
                    build_location_path
                ),
            )

        quantity_before = Decimal(
            batch.quantity
        )

        quantity_after = (
            quantity_before
            - quantity_in_batch_unit
        )

        batch.quantity = (
            quantity_after
        )

        if quantity_after <= 0:
            batch.quantity = Decimal(
                "0"
            )

            batch.is_active = False

        movement = InventoryMovement(
            household_id=(
                batch.household_id
            ),
            inventory_batch=batch,
            movement_type=action,
            quantity_delta=(
                -quantity_in_batch_unit
            ),
            unit=batch.unit,
            quantity_before=(
                quantity_before
            ),
            quantity_after=(
                batch.quantity
            ),
            created_by_user_id=(
                current_user.id
            ),
            note=(
                form.note.data.strip()
                if form.note.data
                else None
            ),
        )

        db.session.add(
            movement
        )

        db.session.commit()

        flash(
            translate(
                (
                    "movement_consumed"
                    if action == "consume"
                    else "movement_discarded"
                )
            ),
            "success",
        )

        return redirect(
            url_for(
                "inventory.inventory_list"
            )
        )

    return render_template(
        "inventory/batch_action.html",
        form=form,
        batch=batch,
        action=action,
        build_location_path=(
            build_location_path
        ),
    )


@bp.route(
    "/batches/<uuid:public_id>/adjust",
    methods=[
        "GET",
        "POST",
    ],
)
@login_required
def batch_adjust(
    public_id,
):
    batch = get_batch_or_404(
        public_id
    )

    form = BatchAdjustmentForm()

    form.quantity.label.text = (
        translate(
            "movement_actual_quantity"
        )
    )

    form.note.label.text = (
        translate(
            "inventory_field_note"
        )
    )

    form.submit.label.text = (
        translate(
            "movement_adjust"
        )
    )

    if not form.is_submitted():
        form.quantity.data = (
            batch.quantity
        )

    if form.validate_on_submit():
        new_quantity = Decimal(
            form.quantity.data
        )

        quantity_before = Decimal(
            batch.quantity
        )

        quantity_delta = (
            new_quantity
            - quantity_before
        )

        batch.quantity = (
            new_quantity
        )

        batch.is_active = (
            new_quantity > 0
        )

        movement = InventoryMovement(
            household_id=(
                batch.household_id
            ),
            inventory_batch=batch,
            movement_type="adjustment",
            quantity_delta=(
                quantity_delta
            ),
            unit=batch.unit,
            quantity_before=(
                quantity_before
            ),
            quantity_after=(
                new_quantity
            ),
            created_by_user_id=(
                current_user.id
            ),
            note=(
                form.note.data.strip()
                if form.note.data
                else None
            ),
        )

        db.session.add(
            movement
        )

        db.session.commit()

        flash(
            translate(
                "movement_adjusted"
            ),
            "success",
        )

        return redirect(
            url_for(
                "inventory.inventory_list"
            )
        )

    return render_template(
        "inventory/batch_action.html",
        form=form,
        batch=batch,
        action="adjust",
        build_location_path=(
            build_location_path
        ),
    )


@bp.route(
    "/batches/<uuid:public_id>/transfer",
    methods=[
        "GET",
        "POST",
    ],
)
@login_required
def batch_transfer(
    public_id,
):
    batch = get_batch_or_404(
        public_id
    )

    form = BatchTransferForm()

    form.storage_location_id.label.text = (
        translate(
            "inventory_field_location"
        )
    )

    form.note.label.text = (
        translate(
            "inventory_field_note"
        )
    )

    form.submit.label.text = (
        translate(
            "movement_transfer"
        )
    )

    form.storage_location_id.choices = (
        get_storage_location_choices(
            batch.household_id
        )
    )

    if not form.is_submitted():
        form.storage_location_id.data = (
            batch.storage_location_id
        )

    if form.validate_on_submit():
        target_location = db.session.get(
            StorageLocation,
            form.storage_location_id.data,
        )

        if (
            target_location is None
            or target_location.household_id
            != batch.household_id
            or not target_location.is_active
        ):
            abort(400)

        old_location = (
            build_location_path(
                batch.storage_location
            )
        )

        new_location = (
            build_location_path(
                target_location
            )
        )

        user_note = (
            form.note.data.strip()
            if form.note.data
            else ""
        )

        movement_note = (
            f"{old_location} -> "
            f"{new_location}"
        )

        if user_note:
            movement_note += (
                f" | {user_note}"
            )

        quantity_before = Decimal(
            batch.quantity
        )

        batch.storage_location = (
            target_location
        )

        movement = InventoryMovement(
            household_id=(
                batch.household_id
            ),
            inventory_batch=batch,
            movement_type="transfer",
            quantity_delta=Decimal(
                "0"
            ),
            unit=batch.unit,
            quantity_before=(
                quantity_before
            ),
            quantity_after=(
                quantity_before
            ),
            created_by_user_id=(
                current_user.id
            ),
            note=movement_note,
        )

        db.session.add(
            movement
        )

        db.session.commit()

        flash(
            translate(
                "movement_transferred"
            ),
            "success",
        )

        return redirect(
            url_for(
                "inventory.inventory_list"
            )
        )

    return render_template(
        "inventory/batch_action.html",
        form=form,
        batch=batch,
        action="transfer",
        build_location_path=(
            build_location_path
        ),
    )


@bp.get("/stock-rules")
@login_required
def stock_rules():
    household_id = (
        get_current_household_id()
    )

    rules = db.session.scalars(
        select(StockRule)
        .where(
            StockRule.household_id
            == household_id
        )
        .order_by(
            StockRule.is_active.desc(),
            StockRule.id,
        )
    ).all()

    return render_template(
        "inventory/stock_rules.html",
        rules=rules,
        get_ingredient_display_name=(
            get_ingredient_display_name
        ),
    )


@bp.route(
    "/stock-rules/new",
    methods=[
        "GET",
        "POST",
    ],
)
@login_required
def stock_rule_new():
    household_id = (
        get_current_household_id()
    )

    form = StockRuleForm()

    form.ingredient_id.label.text = (
        translate(
            "inventory_field_ingredient"
        )
    )

    form.minimum_quantity.label.text = (
        translate(
            "stock_rule_minimum_quantity"
        )
    )

    form.unit_id.label.text = (
        translate(
            "inventory_field_unit"
        )
    )

    form.note.label.text = (
        translate(
            "inventory_field_note"
        )
    )

    form.submit.label.text = (
        translate("save")
    )

    form.ingredient_id.choices = (
        get_ingredient_choices()
    )

    selected_ingredient_id = (
        form.ingredient_id.data
        if form.ingredient_id.data
        else None
    )

    if selected_ingredient_id:
        form.unit_id.choices = (
            get_unit_choices(
                selected_ingredient_id
            )
        )
    else:
        form.unit_id.choices = []

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

        existing_rule = db.session.scalar(
            select(StockRule)
            .where(
                StockRule.household_id
                == household_id,
                StockRule.ingredient_id
                == ingredient.id,
            )
        )

        if existing_rule is not None:
            flash(
                translate(
                    "stock_rule_exists"
                ),
                "error",
            )

            return render_template(
                "inventory/stock_rule_form.html",
                form=form,
                page_title=translate(
                    "stock_rule_new_title"
                ),
            )

        unit = db.session.get(
            Unit,
            form.unit_id.data,
        )

        if unit is None:
            abort(400)

        allowed_unit = db.session.scalar(
            select(IngredientUnit)
            .where(
                IngredientUnit.ingredient_id
                == ingredient.id,
                IngredientUnit.unit_id
                == unit.id,
            )
        )

        if allowed_unit is None:
            abort(400)

        rule = StockRule(
            household_id=household_id,
            ingredient_id=ingredient.id,
            minimum_quantity=(
                form.minimum_quantity.data
            ),
            unit_id=unit.id,
            note=(
                form.note.data.strip()
                if form.note.data
                else None
            ),
            is_active=True,
        )

        db.session.add(rule)
        db.session.commit()

        flash(
            translate(
                "stock_rule_created"
            ),
            "success",
        )

        return redirect(
            url_for(
                "inventory.stock_rules"
            )
        )

    return render_template(
        "inventory/stock_rule_form.html",
        form=form,
        page_title=translate(
            "stock_rule_new_title"
        ),
    )


@bp.route(
    "/stock-rules/<uuid:public_id>/edit",
    methods=[
        "GET",
        "POST",
    ],
)
@login_required
def stock_rule_edit(
    public_id,
):
    rule = get_stock_rule_or_404(
        public_id
    )

    form = StockRuleForm(
        obj=rule
    )

    form.ingredient_id.label.text = (
        translate(
            "inventory_field_ingredient"
        )
    )

    form.minimum_quantity.label.text = (
        translate(
            "stock_rule_minimum_quantity"
        )
    )

    form.unit_id.label.text = (
        translate(
            "inventory_field_unit"
        )
    )

    form.note.label.text = (
        translate(
            "inventory_field_note"
        )
    )

    form.submit.label.text = (
        translate("save")
    )

    form.ingredient_id.choices = (
        get_ingredient_choices()
    )

    if not form.is_submitted():
        form.ingredient_id.data = (
            rule.ingredient_id
        )

        form.unit_id.data = (
            rule.unit_id
        )

    selected_ingredient_id = (
        form.ingredient_id.data
        or rule.ingredient_id
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

        unit = db.session.get(
            Unit,
            form.unit_id.data,
        )

        if (
            ingredient is None
            or unit is None
        ):
            abort(400)

        duplicate = db.session.scalar(
            select(StockRule)
            .where(
                StockRule.household_id
                == rule.household_id,
                StockRule.ingredient_id
                == ingredient.id,
                StockRule.id
                != rule.id,
            )
        )

        if duplicate is not None:
            flash(
                translate(
                    "stock_rule_exists"
                ),
                "error",
            )

            return render_template(
                "inventory/stock_rule_form.html",
                form=form,
                page_title=translate(
                    "stock_rule_edit_title"
                ),
            )

        allowed_unit = db.session.scalar(
            select(IngredientUnit)
            .where(
                IngredientUnit.ingredient_id
                == ingredient.id,
                IngredientUnit.unit_id
                == unit.id,
            )
        )

        if allowed_unit is None:
            abort(400)

        rule.ingredient_id = (
            ingredient.id
        )

        rule.minimum_quantity = (
            form.minimum_quantity.data
        )

        rule.unit_id = unit.id

        rule.note = (
            form.note.data.strip()
            if form.note.data
            else None
        )

        db.session.commit()

        flash(
            translate(
                "stock_rule_updated"
            ),
            "success",
        )

        return redirect(
            url_for(
                "inventory.stock_rules"
            )
        )

    return render_template(
        "inventory/stock_rule_form.html",
        form=form,
        page_title=translate(
            "stock_rule_edit_title"
        ),
    )


@bp.post(
    "/stock-rules/<uuid:public_id>/toggle"
)
@login_required
def stock_rule_toggle(
    public_id,
):
    rule = get_stock_rule_or_404(
        public_id
    )

    rule.is_active = (
        not rule.is_active
    )

    db.session.commit()

    flash(
        translate(
            (
                "stock_rule_reactivated"
                if rule.is_active
                else "stock_rule_deactivated"
            )
        ),
        "success",
    )

    return redirect(
        url_for(
            "inventory.stock_rules"
        )
    )


@bp.get("/movements")
@login_required
def movements():
    household_id = (
        get_current_household_id()
    )

    movement_rows = db.session.scalars(
        select(InventoryMovement)
        .where(
            InventoryMovement.household_id
            == household_id
        )
        .order_by(
            InventoryMovement.created_at
            .desc(),
            InventoryMovement.id.desc(),
        )
    ).all()

    return render_template(
        "inventory/movements.html",
        movements=movement_rows,
        get_ingredient_display_name=(
            get_ingredient_display_name
        ),
        build_location_path=(
            build_location_path
        ),
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
            InventoryBatch.ingredient_id,
            InventoryBatch.expiration_date
            .asc()
            .nullslast(),
            InventoryBatch.created_at,
        )
    ).all()

    stock_rules = db.session.scalars(
        select(StockRule)
        .where(
            StockRule.household_id
            == household_id,
            StockRule.is_active.is_(
                True
            ),
        )
    ).all()

    stock_rule_by_ingredient = {
        rule.ingredient_id: rule
        for rule in stock_rules
    }

    today = date.today()

    expiring_limit = (
        today
        + timedelta(
            days=EXPIRING_SOON_DAYS
        )
    )

    grouped = {}

    for batch in batches:
        ingredient = batch.ingredient

        if ingredient.id not in grouped:
            grouped[ingredient.id] = {
                "ingredient": ingredient,
                "name": (
                    get_ingredient_display_name(
                        ingredient
                    )
                ),
                "batches": [],
                "totals": {},
                "search_text": "",
                "has_expired": False,
                "has_expiring": False,
                "is_low_stock": False,
                "stock_rule": None,
            }

        group = grouped[
            ingredient.id
        ]

        group["batches"].append(
            batch
        )

        batch.expiry_status = None

        if batch.expiration_date:
            if (
                batch.expiration_date
                < today
            ):
                batch.expiry_status = (
                    "expired"
                )

                group[
                    "has_expired"
                ] = True

            elif (
                batch.expiration_date
                <= expiring_limit
            ):
                batch.expiry_status = (
                    "expiring"
                )

                group[
                    "has_expiring"
                ] = True

        dimension = (
            batch.unit.dimension
        )

        base_quantity = (
            Decimal(batch.quantity)
            * Decimal(
                batch.unit.factor_to_base
            )
        )

        group["totals"].setdefault(
            dimension,
            Decimal("0"),
        )

        group["totals"][dimension] += (
            base_quantity
        )

    inventory_groups = []

    for group in grouped.values():
        ingredient = group[
            "ingredient"
        ]

        display_totals = []

        for dimension, base_quantity in (
            group["totals"].items()
        ):
            display_total = (
                build_inventory_display_total(
                    dimension,
                    base_quantity,
                    ingredient,
                )
            )

            if display_total is not None:
                display_totals.append(
                    display_total
                )

        search_parts = [
            group["name"],
            ingredient.canonical_key,
        ]

        for batch in group["batches"]:
            if batch.product is not None:
                search_parts.append(
                    batch.product.name
                )

                if batch.product.brand:
                    search_parts.append(
                        batch.product.brand
                    )

                for barcode in (
                    batch.product.barcodes
                ):
                    search_parts.append(
                        barcode.barcode
                    )

            search_parts.append(
                build_location_path(
                    batch.storage_location
                )
            )

        group["display_totals"] = (
            display_totals
        )

        stock_rule = (
            stock_rule_by_ingredient.get(
                ingredient.id
            )
        )

        if stock_rule is not None:
            rule_dimension = (
                stock_rule.unit.dimension
            )

            current_base_quantity = (
                group["totals"].get(
                    rule_dimension,
                    Decimal("0"),
                )
            )

            minimum_base_quantity = (
                Decimal(
                    stock_rule.minimum_quantity
                )
                * Decimal(
                    stock_rule.unit
                    .factor_to_base
                )
            )

            group["is_low_stock"] = (
                current_base_quantity
                < minimum_base_quantity
            )

            group["stock_rule"] = {
                "quantity": (
                    format_decimal_quantity(
                        stock_rule
                        .minimum_quantity
                    )
                ),
                "symbol": (
                    stock_rule.unit.symbol
                ),
            }

        group["search_text"] = " ".join(
            search_parts
        )

        inventory_groups.append(
            group
        )

    inventory_groups.sort(
        key=lambda item: (
            item["name"].lower()
        )
    )

    return render_template(
        "inventory/inventory_list.html",
        inventory_groups=(
            inventory_groups
        ),
        build_location_path=(
            build_location_path
        ),
    )


@bp.get("/api/ingredient-units")
@login_required
def ingredient_units_api():
    ingredient_id = request.args.get(
        "ingredient_id",
        type=int,
    )

    if not ingredient_id:
        return jsonify(
            units=[],
            default_unit_id=None,
        )

    ingredient = db.session.get(
        Ingredient,
        ingredient_id,
    )

    if (
        ingredient is None
        or not ingredient.is_active
    ):
        abort(404)

    mappings = db.session.scalars(
        select(IngredientUnit)
        .where(
            IngredientUnit.ingredient_id
            == ingredient.id
        )
        .order_by(
            IngredientUnit.sort_order,
            IngredientUnit.id,
        )
    ).all()

    units = []

    for mapping in mappings:
        unit = mapping.unit

        name = next(
            (
                translation.name
                for translation
                in unit.translations
                if translation.language_code
                == current_user
                .preferred_language
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

        units.append(
            {
                "id": unit.id,
                "label": (
                    f"{name} "
                    f"({unit.symbol})"
                ),
            }
        )

    return jsonify(
        units=units,
        default_unit_id=(
            ingredient.default_unit_id
        ),
    )

@bp.get("/api/barcode-lookup")
@login_required
def barcode_lookup_api():
    barcode = (
        request.args.get(
            "barcode",
            "",
        )
        .strip()
    )

    if not barcode:
        return jsonify(
            found=False,
            product=None,
        )

    household_id = (
        get_current_household_id()
    )

    product_barcode = db.session.scalar(
        select(ProductBarcode)
        .join(
            Product,
            Product.id
            == ProductBarcode.product_id,
        )
        .where(
            ProductBarcode.barcode
            == barcode,
            Product.household_id
            == household_id,
            Product.is_active.is_(True),
        )
    )

    if product_barcode is None:
        return jsonify(
            found=False,
            product=None,
        )

    product = (
        product_barcode.product
    )

    ingredient_name = next(
        (
            translation.name
            for translation
            in product.ingredient.translations
            if translation.language_code
            == current_user.preferred_language
        ),
        None,
    )

    if ingredient_name is None:
        ingredient_name = next(
            (
                translation.name
                for translation
                in product.ingredient.translations
                if translation.language_code
                == "hu"
            ),
            product.ingredient.canonical_key,
        )

    return jsonify(
        found=True,
        product={
            "id": product.id,
            "public_id": str(
                product.public_id
            ),
            "name": product.name,
            "brand": (
                product.brand
                or ""
            ),
            "ingredient_id": (
                product.ingredient_id
            ),
            "ingredient_name": (
                ingredient_name
            ),
            "package_quantity": (
                str(
                    product.package_quantity
                )
                if product.package_quantity
                is not None
                else None
            ),
            "package_unit_id": (
                product.package_unit_id
            ),
            "package_unit_symbol": (
                product.package_unit.symbol
                if product.package_unit
                else None
            ),
            "barcode": (
                product_barcode.barcode
            ),
        },
    )
