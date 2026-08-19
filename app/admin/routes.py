import csv
import io
import re
import unicodedata
from flask import (
    Response,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import (
    current_user,
    login_required,
)
from sqlalchemy import (
    func,
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
    Ingredient,
    IngredientAlias,
    IngredientCategory,
    IngredientTranslation,
    IngredientUnit,
    InventoryBatch,
    Product,
    ProductBarcode,
    RecipeTag,
    StorageLocation,
    Unit,
    User,
)

from . import bp
from .forms import (
    HouseholdMemberForm,
    IngredientAdminForm,
    NewHouseholdUserForm,
    ProfileForm,
)

from app.recipes.forms import (
    RecipeTagForm,
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


def normalize_text(
    value,
):
    value = (
        unicodedata.normalize(
            "NFKD",
            value,
        )
        .encode(
            "ascii",
            "ignore",
        )
        .decode("ascii")
        .lower()
        .strip()
    )

    value = re.sub(
        r"[^a-z0-9]+",
        "_",
        value,
    )

    return value.strip("_")


def get_ingredient_name(
    ingredient,
    language_code=None,
):
    language_code = (
        language_code
        or current_user.preferred_language
        or "hu"
    )

    name = next(
        (
            translation.name
            for translation
            in ingredient.translations
            if translation.language_code
            == language_code
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


def get_category_name(
    category,
):
    name = next(
        (
            translation.name
            for translation
            in category.translations
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
                in category.translations
                if translation.language_code
                == "hu"
            ),
            None,
        )

    return (
        name
        or category.canonical_key
    )


def build_category_choices():
    categories = db.session.scalars(
        select(IngredientCategory)
        .where(
            IngredientCategory.is_active.is_(
                True
            )
        )
        .order_by(
            IngredientCategory.sort_order,
            IngredientCategory.id,
        )
    ).all()

    by_parent = {}

    for category in categories:
        by_parent.setdefault(
            category.parent_id,
            [],
        ).append(category)

    choices = [
        (
            0,
            translate(
                "ingredient_admin_no_category"
            ),
        )
    ]

    def append_children(
        parent_id,
        depth,
    ):
        children = by_parent.get(
            parent_id,
            [],
        )

        children.sort(
            key=lambda item: (
                item.sort_order,
                get_category_name(
                    item
                ).lower(),
            )
        )

        for category in children:
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
                    category.id,
                    (
                        f"{prefix}"
                        f"{marker}"
                        f"{get_category_name(category)}"
                    ),
                )
            )

            append_children(
                category.id,
                depth + 1,
            )

    append_children(
        None,
        0,
    )

    return choices


def build_unit_choices():
    units = db.session.scalars(
        select(Unit)
        .where(
            Unit.is_active.is_(
                True
            )
        )
        .order_by(
            Unit.dimension,
            Unit.sort_order,
            Unit.code,
        )
    ).all()

    choices = []

    for unit in units:
        dimension_label = translate(
            f"unit_dimension_{unit.dimension}"
        )

        unit_name = next(
            (
                translation.name
                for translation
                in unit.translations
                if translation.language_code
                == current_user.preferred_language
            ),
            None,
        )

        if unit_name is None:
            unit_name = next(
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
                (
                    f"{unit_name} "
                    f"({unit.symbol}) "
                    f"— {dimension_label}"
                ),
            )
        )

    return choices


def split_aliases(
    value,
):
    if not value:
        return []

    aliases = []

    for line in value.splitlines():
        for part in line.split(","):
            alias = part.strip()

            if alias:
                aliases.append(alias)

    return aliases


def set_translation(
    ingredient,
    language_code,
    name,
):
    name = (
        name.strip()
        if name
        else ""
    )

    existing = next(
        (
            translation
            for translation
            in ingredient.translations
            if translation.language_code
            == language_code
        ),
        None,
    )

    if name:
        if existing is None:
            existing = (
                IngredientTranslation(
                    ingredient=ingredient,
                    language_code=(
                        language_code
                    ),
                    name=name,
                )
            )

            db.session.add(
                existing
            )
        else:
            existing.name = name

    elif existing is not None:
        db.session.delete(
            existing
        )


def replace_aliases(
    ingredient,
    language_code,
    raw_value,
):
    for alias in list(
        ingredient.aliases
    ):
        if (
            alias.language_code
            == language_code
        ):
            db.session.delete(
                alias
            )

    seen = set()

    for alias_text in split_aliases(
        raw_value
    ):
        normalized = normalize_text(
            alias_text
        )

        if (
            not normalized
            or normalized in seen
        ):
            continue

        seen.add(
            normalized
        )

        db.session.add(
            IngredientAlias(
                ingredient=ingredient,
                language_code=(
                    language_code
                ),
                alias=alias_text,
                normalized_alias=(
                    normalized
                ),
            )
        )


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


@bp.get("/")
@login_required
def index():
    membership = (
        get_admin_membership()
    )

    members = db.session.scalars(
        select(HouseholdMember)
        .where(
            HouseholdMember.household_id
            == membership.household_id
        )
    ).all()

    total_users = len(
        members
    )

    active_users = sum(
        1
        for member in members
        if member.is_active
    )

    total_ingredients = db.session.scalar(
        select(
            func.count(
                Ingredient.id
            )
        )
    ) or 0

    active_ingredients = db.session.scalar(
        select(
            func.count(
                Ingredient.id
            )
        )
        .where(
            Ingredient.is_active.is_(
                True
            )
        )
    ) or 0

    return render_template(
        "admin/index.html",
        total_users=total_users,
        active_users=active_users,
        total_ingredients=(
            total_ingredients
        ),
        active_ingredients=(
            active_ingredients
        ),
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
        if (
            admin_membership.role
            == "admin"
            and form.role.data
            == "owner"
        ):
            abort(403)
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

    if admin_membership.role == "admin":
        form.role.choices = [
            choice
            for choice in form.role.choices
            if choice[0] != "owner"
        ]

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


@bp.get("/ingredients")
@login_required
def ingredients():
    get_admin_membership()

    page = request.args.get(
        "page",
        1,
        type=int,
    )

    if page < 1:
        page = 1

    search_text = (
        request.args.get(
            "q",
            "",
        )
        .strip()
    )

    per_page = 50

    filters = []

    if search_text:
        pattern = (
            f"%{search_text}%"
        )

        filters.append(
            or_(
                Ingredient.canonical_key
                .ilike(pattern),

                Ingredient.translations.any(
                    IngredientTranslation.name
                    .ilike(pattern)
                ),

                Ingredient.aliases.any(
                    IngredientAlias.alias
                    .ilike(pattern)
                ),
            )
        )

    count_query = select(
        func.count(
            Ingredient.id
        )
    )

    if filters:
        count_query = (
            count_query.where(
                *filters
            )
        )

    total_ingredients = (
        db.session.scalar(
            count_query
        )
        or 0
    )

    total_pages = max(
        1,
        (
            total_ingredients
            + per_page
            - 1
        )
        // per_page,
    )

    if page > total_pages:
        page = total_pages

    ingredient_query = (
        select(Ingredient)
        .order_by(
            Ingredient.is_active.desc(),
            Ingredient.canonical_key,
        )
    )

    if filters:
        ingredient_query = (
            ingredient_query.where(
                *filters
            )
        )

    ingredient_rows = db.session.scalars(
        ingredient_query
        .offset(
            (
                page - 1
            )
            * per_page
        )
        .limit(
            per_page
        )
    ).all()

    return render_template(
        "admin/ingredients.html",
        ingredients=(
            ingredient_rows
        ),
        get_ingredient_name=(
            get_ingredient_name
        ),
        get_category_name=(
            get_category_name
        ),
        page=page,
        total_pages=total_pages,
        total_ingredients=(
            total_ingredients
        ),
        search_text=search_text,
    )


@bp.route(
    "/ingredients/new",
    methods=[
        "GET",
        "POST",
    ],
)
@login_required
def ingredient_new():
    get_admin_membership()

    form = IngredientAdminForm()

    form.name_hu.label.text = (
        translate(
            "ingredient_admin_name_hu"
        )
    )

    form.name_en.label.text = (
        translate(
            "ingredient_admin_name_en"
        )
    )

    form.category_id.label.text = (
        translate(
            "ingredient_admin_category"
        )
    )

    form.default_unit_id.label.text = (
        translate(
            "ingredient_admin_default_unit"
        )
    )

    form.allowed_unit_ids.label.text = (
        translate(
            "ingredient_admin_allowed_units"
        )
    )

    form.aliases_hu.label.text = (
        translate(
            "ingredient_admin_aliases_hu"
        )
    )

    form.aliases_en.label.text = (
        translate(
            "ingredient_admin_aliases_en"
        )
    )

    form.is_active.label.text = (
        translate(
            "admin_active"
        )
    )

    form.submit.label.text = (
        translate("save")
    )

    form.category_id.choices = (
        build_category_choices()
    )

    unit_choices = (
        build_unit_choices()
    )

    form.default_unit_id.choices = (
        unit_choices
    )

    form.allowed_unit_ids.choices = (
        unit_choices
    )

    if form.validate_on_submit():
        allowed_unit_ids = set(
            form.allowed_unit_ids.data
        )

        if (
            form.default_unit_id.data
            not in allowed_unit_ids
        ):
            form.allowed_unit_ids.errors.append(
                translate(
                    "ingredient_admin_default_must_be_allowed"
                )
            )

            return render_template(
                "admin/ingredient_form.html",
                form=form,
                page_title=translate(
                    "ingredient_admin_new"
                ),
            )

        canonical_source = (
            form.name_en.data
            or form.name_hu.data
        )

        canonical_key = (
            normalize_text(
                canonical_source
            )
        )

        existing = db.session.scalar(
            select(Ingredient)
            .where(
                Ingredient.canonical_key
                == canonical_key
            )
        )

        if existing is not None:
            form.name_hu.errors.append(
                translate(
                    "ingredient_admin_exists"
                )
            )

            return render_template(
                "admin/ingredient_form.html",
                form=form,
                page_title=translate(
                    "ingredient_admin_new"
                ),
            )

        category = None

        if form.category_id.data:
            category = db.session.get(
                IngredientCategory,
                form.category_id.data,
            )

        default_unit = db.session.get(
            Unit,
            form.default_unit_id.data,
        )

        if default_unit is None:
            abort(400)

        ingredient = Ingredient(
            canonical_key=canonical_key,
            category=category,
            default_unit=default_unit,
            is_active=(
                form.is_active.data
            ),
        )

        db.session.add(
            ingredient
        )

        db.session.flush()

        set_translation(
            ingredient,
            "hu",
            form.name_hu.data,
        )

        set_translation(
            ingredient,
            "en",
            form.name_en.data,
        )

        replace_aliases(
            ingredient,
            "hu",
            form.aliases_hu.data,
        )

        replace_aliases(
            ingredient,
            "en",
            form.aliases_en.data,
        )

        for sort_order, unit_id in enumerate(
            form.allowed_unit_ids.data,
            start=10,
        ):
            db.session.add(
                IngredientUnit(
                    ingredient=ingredient,
                    unit_id=unit_id,
                    is_default=(
                        unit_id
                        == form.default_unit_id.data
                    ),
                    sort_order=sort_order,
                )
            )

        db.session.commit()

        flash(
            translate(
                "ingredient_admin_created"
            ),
            "success",
        )

        return_to = request.args.get(
            "return_to",
            "",
        )

        if (
            return_to
            == "product_new"
        ):
            return redirect(
                url_for(
                    "inventory.product_new",
                    ingredient_id=ingredient.id,
                )
            )

        if (
            return_to
            == "batch_new"
        ):
            return redirect(
                url_for(
                    "inventory.batch_new",
                    ingredient_id=ingredient.id,
                )
            )

        return redirect(
            url_for(
                "admin.ingredients"
            )
        )

    return render_template(
        "admin/ingredient_form.html",
        form=form,
        page_title=translate(
            "ingredient_admin_new"
        ),
    )


@bp.route(
    "/ingredients/<uuid:public_id>/edit",
    methods=[
        "GET",
        "POST",
    ],
)
@login_required
def ingredient_edit(
    public_id,
):
    get_admin_membership()

    ingredient = db.session.scalar(
        select(Ingredient)
        .where(
            Ingredient.public_id
            == public_id
        )
    )

    if ingredient is None:
        abort(404)

    form = IngredientAdminForm()

    form.name_hu.label.text = (
        translate(
            "ingredient_admin_name_hu"
        )
    )

    form.name_en.label.text = (
        translate(
            "ingredient_admin_name_en"
        )
    )

    form.category_id.label.text = (
        translate(
            "ingredient_admin_category"
        )
    )

    form.default_unit_id.label.text = (
        translate(
            "ingredient_admin_default_unit"
        )
    )

    form.allowed_unit_ids.label.text = (
        translate(
            "ingredient_admin_allowed_units"
        )
    )

    form.aliases_hu.label.text = (
        translate(
            "ingredient_admin_aliases_hu"
        )
    )

    form.aliases_en.label.text = (
        translate(
            "ingredient_admin_aliases_en"
        )
    )

    form.is_active.label.text = (
        translate(
            "admin_active"
        )
    )

    form.submit.label.text = (
        translate("save")
    )

    form.category_id.choices = (
        build_category_choices()
    )

    unit_choices = (
        build_unit_choices()
    )

    form.default_unit_id.choices = (
        unit_choices
    )

    form.allowed_unit_ids.choices = (
        unit_choices
    )

    if not form.is_submitted():
        form.name_hu.data = next(
            (
                item.name
                for item
                in ingredient.translations
                if item.language_code
                == "hu"
            ),
            "",
        )

        form.name_en.data = next(
            (
                item.name
                for item
                in ingredient.translations
                if item.language_code
                == "en"
            ),
            "",
        )

        form.category_id.data = (
            ingredient.category_id
            or 0
        )

        form.default_unit_id.data = (
            ingredient.default_unit_id
        )

        form.allowed_unit_ids.data = [
            item.unit_id
            for item
            in ingredient.allowed_units
        ]

        form.aliases_hu.data = "\n".join(
            item.alias
            for item
            in ingredient.aliases
            if item.language_code
            == "hu"
        )

        form.aliases_en.data = "\n".join(
            item.alias
            for item
            in ingredient.aliases
            if item.language_code
            == "en"
        )

        form.is_active.data = (
            ingredient.is_active
        )

    if form.validate_on_submit():
        allowed_unit_ids = set(
            form.allowed_unit_ids.data
        )

        if (
            form.default_unit_id.data
            not in allowed_unit_ids
        ):
            form.allowed_unit_ids.errors.append(
                translate(
                    "ingredient_admin_default_must_be_allowed"
                )
            )

            return render_template(
                "admin/ingredient_form.html",
                form=form,
                page_title=translate(
                    "ingredient_admin_edit"
                ),
            )

        category = None

        if form.category_id.data:
            category = db.session.get(
                IngredientCategory,
                form.category_id.data,
            )

        default_unit = db.session.get(
            Unit,
            form.default_unit_id.data,
        )

        if default_unit is None:
            abort(400)

        ingredient.category = category
        ingredient.default_unit = (
            default_unit
        )
        ingredient.is_active = (
            form.is_active.data
        )

        set_translation(
            ingredient,
            "hu",
            form.name_hu.data,
        )

        set_translation(
            ingredient,
            "en",
            form.name_en.data,
        )

        replace_aliases(
            ingredient,
            "hu",
            form.aliases_hu.data,
        )

        replace_aliases(
            ingredient,
            "en",
            form.aliases_en.data,
        )

        for mapping in list(
            ingredient.allowed_units
        ):
            db.session.delete(
                mapping
            )

        db.session.flush()

        for sort_order, unit_id in enumerate(
            form.allowed_unit_ids.data,
            start=10,
        ):
            db.session.add(
                IngredientUnit(
                    ingredient=ingredient,
                    unit_id=unit_id,
                    is_default=(
                        unit_id
                        == form.default_unit_id.data
                    ),
                    sort_order=sort_order,
                )
            )

        db.session.commit()

        flash(
            translate(
                "ingredient_admin_updated"
            ),
            "success",
        )

        return redirect(
            url_for(
                "admin.ingredients"
            )
        )

    return render_template(
        "admin/ingredient_form.html",
        form=form,
        page_title=translate(
            "ingredient_admin_edit"
        ),
    )


@bp.post(
    "/ingredients/<uuid:public_id>/toggle"
)
@login_required
def ingredient_toggle(
    public_id,
):
    get_admin_membership()

    ingredient = db.session.scalar(
        select(Ingredient)
        .where(
            Ingredient.public_id
            == public_id
        )
    )

    if ingredient is None:
        abort(404)

    ingredient.is_active = (
        not ingredient.is_active
    )

    db.session.commit()

    return redirect(
        url_for(
            "admin.ingredients"
        )
    )


@bp.get(
    "/data-management"
)
@login_required
def data_management():
    get_admin_membership()

    return render_template(
        "admin/data_management.html"
    )


def csv_response(
    filename,
    rows,
):
    output = io.StringIO(
        newline=""
    )

    output.write(
        "\ufeff"
    )

    writer = csv.writer(
        output,
        delimiter=";",
        quoting=csv.QUOTE_MINIMAL,
        lineterminator="\r\n",
    )

    for row in rows:
        writer.writerow(
            row
        )

    return Response(
        output.getvalue(),
        mimetype=(
            "text/csv; "
            "charset=utf-8"
        ),
        headers={
            "Content-Disposition": (
                f'attachment; '
                f'filename="{filename}"'
            ),
        },
    )

@bp.get(
    "/data-management/export-inventory"
)
@login_required
def export_inventory():
    membership = (
        get_admin_membership()
    )

    household_id = (
        membership.household_id
    )

    batches = db.session.scalars(
        select(InventoryBatch)
        .where(
            InventoryBatch.household_id
            == household_id,
        )
        .order_by(
            InventoryBatch.id,
        )
    ).all()

    rows = [
        (
            "Alapanyag",
            "Termék",
            "Márka",
            "Vonalkód",
            "Mennyiség",
            "Mértékegység",
            "Tárolási hely",
            "Vásárlás dátuma",
            "Lejárat dátuma",
            "Aktív",
            "Megjegyzés",
        )
    ]

    for batch in batches:
        ingredient_name = (
            next(
                (
                    translation.name
                    for translation
                    in batch.ingredient.translations
                    if translation.language_code
                    == (
                        current_user
                        .preferred_language
                        or "hu"
                    )
                ),
                None,
            )
            or batch.ingredient.canonical_key
        )

        product_name = (
            batch.product.name
            if batch.product
            else ""
        )

        brand = (
            batch.product.brand
            if batch.product
            else ""
        )

        barcode = ""

        if (
            batch.product
            and batch.product.barcodes
        ):
            barcode = (
                batch.product.barcodes[0]
                .barcode
            )

        location_path = ""

        if batch.storage_location:
            parts = []

            current_location = (
                batch.storage_location
            )

            while (
                current_location
                is not None
            ):
                parts.append(
                    current_location.name
                )

                current_location = (
                    current_location.parent
                )

            location_path = " → ".join(
                reversed(parts)
            )

        rows.append(
            (
                ingredient_name,
                product_name,
                brand,
                barcode,
                batch.quantity,
                (
                    batch.unit.symbol
                    if batch.unit
                    else ""
                ),
                location_path,
                (
                    batch.purchase_date
                    .isoformat()
                    if batch.purchase_date
                    else ""
                ),
                (
                    batch.expiration_date
                    .isoformat()
                    if batch.expiration_date
                    else ""
                ),
                (
                    "Igen"
                    if batch.is_active
                    else "Nem"
                ),
                batch.note or "",
            )
        )

    return csv_response(
        "homepantry-inventory.csv",
        rows,
    )

@bp.get(
    "/data-management/export-products"
)
@login_required
def export_products():
    membership = (
        get_admin_membership()
    )

    household_id = (
        membership.household_id
    )

    products = db.session.scalars(
        select(Product)
        .where(
            Product.household_id
            == household_id,
        )
        .order_by(
            Product.id,
        )
    ).all()

    rows = [
        (
            "Termék",
            "Márka",
            "Alapanyag",
            "Vonalkódok",
            "Csomag mennyiség",
            "Csomag mértékegység",
            "Magyar név",
            "Angol név",
            "Magyar általános név",
            "Angol általános név",
            "Magyar összetevők",
            "Angol összetevők",
            "Külső forrás",
            "Külső azonosító",
            "Aktív",
        )
    ]

    for product in products:
        ingredient_name = ""

        if product.ingredient:
            ingredient_name = (
                next(
                    (
                        translation.name
                        for translation
                        in product.ingredient.translations
                        if translation.language_code
                        == (
                            current_user
                            .preferred_language
                            or "hu"
                        )
                    ),
                    None,
                )
                or product.ingredient.canonical_key
            )

        barcodes = ", ".join(
            barcode.barcode
            for barcode in product.barcodes
            if barcode.barcode
        )

        rows.append(
            (
                product.name,
                product.brand or "",
                ingredient_name,
                barcodes,
                (
                    product.package_quantity
                    if product.package_quantity
                    is not None
                    else ""
                ),
                (
                    product.package_unit.symbol
                    if product.package_unit
                    else ""
                ),
                product.name_hu or "",
                product.name_en or "",
                product.generic_name_hu or "",
                product.generic_name_en or "",
                product.ingredients_text_hu or "",
                product.ingredients_text_en or "",
                product.external_source or "",
                product.external_source_id or "",
                (
                    "Igen"
                    if product.is_active
                    else "Nem"
                ),
            )
        )

    return csv_response(
        "homepantry-products.csv",
        rows,
    )

def configure_recipe_tag_form(
    form,
):
    form.name.label.text = translate(
        "recipe_tag_name"
    )

    form.key.label.text = translate(
        "recipe_tag_key"
    )

    form.group_name.label.text = translate(
        "recipe_tag_group"
    )

    form.sort_order.label.text = translate(
        "recipe_tag_sort_order"
    )

    form.is_active.label.text = translate(
        "admin_active"
    )

    form.submit.label.text = translate(
        "save"
    )

    form.group_name.choices = [
        (
            "food_type",
            translate(
                "recipe_tag_group_food_type"
            ),
        ),
        (
            "cuisine",
            translate(
                "recipe_tag_group_cuisine"
            ),
        ),
        (
            "diet",
            translate(
                "recipe_tag_group_diet"
            ),
        ),
        (
            "other",
            translate(
                "recipe_tag_group_other"
            ),
        ),
    ]


@bp.get("/recipe-tags")
@login_required
def recipe_tags():
    get_admin_membership()

    tags = db.session.scalars(
        select(RecipeTag)
        .order_by(
            RecipeTag.group_name,
            RecipeTag.sort_order,
            RecipeTag.name,
            RecipeTag.id,
        )
    ).all()

    return render_template(
        "admin/recipe_tags.html",
        tags=tags,
    )


@bp.route(
    "/recipe-tags/new",
    methods=[
        "GET",
        "POST",
    ],
)
@login_required
def recipe_tag_new():
    get_admin_membership()

    form = RecipeTagForm()

    configure_recipe_tag_form(
        form
    )

    if form.validate_on_submit():
        key = (
            form.key.data
            .strip()
            .lower()
        )

        existing = db.session.scalar(
            select(RecipeTag)
            .where(
                RecipeTag.key
                == key
            )
        )

        if existing is not None:
            form.key.errors.append(
                translate(
                    "recipe_tag_key_exists"
                )
            )
        else:
            tag = RecipeTag(
                key=key,
                name=(
                    form.name.data
                    .strip()
                ),
                group_name=(
                    form.group_name.data
                ),
                sort_order=(
                    form.sort_order.data
                ),
                is_active=(
                    form.is_active.data
                ),
            )

            db.session.add(
                tag
            )

            db.session.commit()

            flash(
                translate(
                    "recipe_tag_created"
                ),
                "success",
            )

            return redirect(
                url_for(
                    "admin.recipe_tags"
                )
            )

    return render_template(
        "admin/recipe_tag_form.html",
        form=form,
        page_title=translate(
            "recipe_tag_new"
        ),
    )


@bp.route(
    "/recipe-tags/<int:tag_id>/edit",
    methods=[
        "GET",
        "POST",
    ],
)
@login_required
def recipe_tag_edit(
    tag_id,
):
    get_admin_membership()

    tag = db.session.get(
        RecipeTag,
        tag_id,
    )

    if tag is None:
        abort(404)

    form = RecipeTagForm(
        obj=tag
    )

    configure_recipe_tag_form(
        form
    )

    if form.validate_on_submit():
        key = (
            form.key.data
            .strip()
            .lower()
        )

        conflict = db.session.scalar(
            select(RecipeTag)
            .where(
                RecipeTag.id
                != tag.id,
                RecipeTag.key
                == key,
            )
        )

        if conflict is not None:
            form.key.errors.append(
                translate(
                    "recipe_tag_key_exists"
                )
            )
        else:
            tag.key = key

            tag.name = (
                form.name.data
                .strip()
            )

            tag.group_name = (
                form.group_name.data
            )

            tag.sort_order = (
                form.sort_order.data
            )

            tag.is_active = (
                form.is_active.data
            )

            db.session.commit()

            flash(
                translate(
                    "recipe_tag_updated"
                ),
                "success",
            )

            return redirect(
                url_for(
                    "admin.recipe_tags"
                )
            )

    return render_template(
        "admin/recipe_tag_form.html",
        form=form,
        page_title=translate(
            "recipe_tag_edit"
        ),
    )


@bp.post(
    "/recipe-tags/<int:tag_id>/toggle"
)
@login_required
def recipe_tag_toggle(
    tag_id,
):
    get_admin_membership()

    tag = db.session.get(
        RecipeTag,
        tag_id,
    )

    if tag is None:
        abort(404)

    tag.is_active = (
        not tag.is_active
    )

    db.session.commit()

    return redirect(
        url_for(
            "admin.recipe_tags"
        )
    )
