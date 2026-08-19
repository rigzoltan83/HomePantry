import unicodedata
from decimal import (
    Decimal,
    InvalidOperation,
)
from flask import (
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import (
    current_user,
    login_required,
)
from sqlalchemy import select

from app.extensions import db
from app.i18n import translate
from app.models import (
    HouseholdMember,
    Ingredient,
    InventoryBatch,
    Recipe,
    RecipeIngredient,
    RecipeTag,
    Unit,
)

from . import bp
from .forms import RecipeForm


def normalize_search_text(
    value,
):
    return (
        unicodedata.normalize(
            "NFKD",
            str(value or ""),
        )
        .encode(
            "ascii",
            "ignore",
        )
        .decode("ascii")
        .lower()
        .strip()
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

def get_recipe_or_404(
    public_id,
):
    household_id = (
        get_current_household_id()
    )

    recipe = db.session.scalar(
        select(Recipe)
        .where(
            Recipe.public_id
            == public_id,
            Recipe.household_id
            == household_id,
        )
    )

    if recipe is None:
        abort(404)

    return recipe

def get_selected_tag_ids():
    selected_tag_ids = set()

    for raw_tag_id in request.form.getlist(
        "recipe_tag_ids"
    ):
        try:
            selected_tag_ids.add(
                int(raw_tag_id)
            )
        except (
            TypeError,
            ValueError,
        ):
            continue

    return selected_tag_ids

def get_recipe_ingredient_rows():
    ingredient_ids = request.form.getlist(
        "ingredient_id"
    )

    ingredient_names = request.form.getlist(
        "ingredient_name"
    )

    quantities = request.form.getlist(
        "ingredient_quantity"
    )

    unit_ids = request.form.getlist(
        "ingredient_unit_id"
    )

    unit_texts = request.form.getlist(
        "ingredient_unit_text"
    )

    row_count = max(
        len(ingredient_ids),
        len(ingredient_names),
        len(quantities),
        len(unit_ids),
        len(unit_texts),
        0,
    )

    rows = []

    for index in range(row_count):
        raw_name = (
            ingredient_names[index]
            if index < len(ingredient_names)
            else ""
        )

        name = raw_name.strip()

        if not name:
            continue

        raw_ingredient_id = (
            ingredient_ids[index]
            if index < len(ingredient_ids)
            else ""
        )

        raw_quantity = (
            quantities[index]
            if index < len(quantities)
            else ""
        )

        raw_unit_id = (
            unit_ids[index]
            if index < len(unit_ids)
            else ""
        )

        raw_unit_text = (
            unit_texts[index]
            if index < len(unit_texts)
            else ""
        )

        ingredient_id = None

        try:
            parsed_ingredient_id = int(
                raw_ingredient_id
            )

            if parsed_ingredient_id > 0:
                ingredient = db.session.get(
                    Ingredient,
                    parsed_ingredient_id,
                )

                if (
                    ingredient is not None
                    and ingredient.is_active
                ):
                    ingredient_id = (
                        ingredient.id
                    )
        except (
            TypeError,
            ValueError,
        ):
            pass

        quantity = None

        if raw_quantity.strip():
            try:
                quantity = Decimal(
                    raw_quantity
                )

                if quantity < 0:
                    quantity = None

            except (
                InvalidOperation,
                ValueError,
            ):
                quantity = None

        unit_id = None

        try:
            parsed_unit_id = int(
                raw_unit_id
            )

            if parsed_unit_id > 0:
                unit = db.session.get(
                    Unit,
                    parsed_unit_id,
                )

                if unit is not None:
                    unit_id = unit.id

        except (
            TypeError,
            ValueError,
        ):
            pass

        unit_text = (
            raw_unit_text.strip()
            or None
        )

        if unit_id is not None:
            unit_text = None

        rows.append(
            {
                "original_name": name,
                "ingredient_id": ingredient_id,
                "quantity": quantity,
                "unit_id": unit_id,
                "unit_text": unit_text,
            }
        )

    return rows

def get_active_recipe_tags():
    return db.session.scalars(
        select(RecipeTag)
        .where(
            RecipeTag.is_active.is_(
                True
            )
        )
        .order_by(
            RecipeTag.group_name,
            RecipeTag.sort_order,
            RecipeTag.name,
            RecipeTag.id,
        )
    ).all()


def build_recipe_tag_groups(
    tags,
):
    groups = {
        "food_type": [],
        "cuisine": [],
        "diet": [],
        "other": [],
    }

    for tag in tags:
        groups.setdefault(
            tag.group_name,
            [],
        ).append(tag)

    return groups


def configure_recipe_form(
    form,
):
    form.title.label.text = translate(
        "recipe_field_title"
    )

    form.difficulty.label.text = translate(
        "recipe_field_difficulty"
    )

    form.servings.label.text = translate(
        "recipe_field_servings"
    )

    form.prep_time_minutes.label.text = translate(
        "recipe_field_prep_time"
    )

    form.cook_time_minutes.label.text = translate(
        "recipe_field_cook_time"
    )

    form.instructions_text.label.text = translate(
        "recipe_field_instructions"
    )

    form.submit.label.text = translate(
        "save"
    )

    form.difficulty.choices = [
        (
            "",
            translate(
                "recipe_difficulty_unspecified"
            ),
        ),
        (
            "easy",
            translate(
                "recipe_difficulty_easy"
            ),
        ),
        (
            "medium",
            translate(
                "recipe_difficulty_medium"
            ),
        ),
        (
            "hard",
            translate(
                "recipe_difficulty_hard"
            ),
        ),
    ]


@bp.get("/")
@login_required
def index():
    household_id = (
        get_current_household_id()
    )

    search_text = (
        request.args.get(
            "q",
            "",
        )
        .strip()
    )

    difficulty = (
        request.args.get(
            "difficulty",
            "",
        )
        .strip()
    )

    max_time = request.args.get(
        "max_time",
        type=int,
    )

    only_available = (
        request.args.get(
            "only_available"
        )
        == "1"
    )

    selected_tag_ids = set()

    for raw_tag_id in request.args.getlist(
        "tag"
    ):
        try:
            selected_tag_ids.add(
                int(raw_tag_id)
            )
        except (
            TypeError,
            ValueError,
        ):
            continue

    available_tags = (
        get_active_recipe_tags()
    )

    tag_groups = (
        build_recipe_tag_groups(
            available_tags
        )
    )

    recipes = db.session.scalars(
        select(Recipe)
        .where(
            Recipe.household_id
            == household_id,
            Recipe.is_active.is_(
                True
            ),
        )
        .order_by(
            Recipe.title,
            Recipe.id,
        )
    ).all()

    available_ingredient_ids = set(
        db.session.scalars(
            select(
                InventoryBatch.ingredient_id
            )
            .where(
                InventoryBatch.household_id
                == household_id,
                InventoryBatch.is_active.is_(
                    True
                ),
                InventoryBatch.quantity > 0,
            )
            .distinct()
        ).all()
    )

    normalized_search = (
        normalize_search_text(
            search_text
        )
    )

    recipe_rows = []

    for recipe in recipes:
        recipe_tag_ids = {
            tag.id
            for tag in recipe.tags
        }

        if (
            selected_tag_ids
            and not selected_tag_ids.issubset(
                recipe_tag_ids
            )
        ):
            continue

        if (
            difficulty
            and recipe.difficulty
            != difficulty
        ):
            continue

        if max_time is not None:
            if (
                recipe.total_time_minutes
                is None
                or recipe.total_time_minutes
                > max_time
            ):
                continue

        searchable_parts = [
            recipe.title,
        ]

        searchable_parts.extend(
            tag.name
            for tag in recipe.tags
        )

        searchable_parts.extend(
            ingredient.original_name
            for ingredient
            in recipe.ingredients
        )

        searchable_text = (
            normalize_search_text(
                " ".join(
                    searchable_parts
                )
            )
        )

        if (
            normalized_search
            and normalized_search
            not in searchable_text
        ):
            continue

        total_ingredients = len(
            recipe.ingredients
        )

        available_count = sum(
            1
            for ingredient
            in recipe.ingredients
            if (
                ingredient.ingredient_id
                is not None
                and ingredient.ingredient_id
                in available_ingredient_ids
            )
        )

        missing_count = (
            total_ingredients
            - available_count
        )

        all_available = (
            total_ingredients > 0
            and missing_count == 0
        )

        if (
            only_available
            and not all_available
        ):
            continue

        match_percent = 0

        if total_ingredients:
            match_percent = round(
                (
                    available_count
                    / total_ingredients
                )
                * 100
            )

        recipe_rows.append(
            {
                "recipe": recipe,
                "available_count": (
                    available_count
                ),
                "total_ingredients": (
                    total_ingredients
                ),
                "missing_count": (
                    missing_count
                ),
                "all_available": (
                    all_available
                ),
                "match_percent": (
                    match_percent
                ),
            }
        )

    recipe_rows.sort(
        key=lambda row: (
            -row["match_percent"],
            row["recipe"].title.lower(),
            row["recipe"].id,
        )
    )

    return render_template(
        "recipes/index.html",
        recipe_rows=recipe_rows,
        search_text=search_text,
        difficulty=difficulty,
        max_time=max_time,
        only_available=only_available,
        tag_groups=tag_groups,
        selected_tag_ids=(
            selected_tag_ids
        ),
    )


@bp.route(
    "/new",
    methods=[
        "GET",
        "POST",
    ],
)
@login_required
def new():
    household_id = (
        get_current_household_id()
    )

    form = RecipeForm()

    available_tags = (
        get_active_recipe_tags()
    )

    tag_groups = (
        build_recipe_tag_groups(
            available_tags
        )
    )

    configure_recipe_form(
        form
    )

    if form.validate_on_submit():
        prep_time = (
            form.prep_time_minutes.data
            or 0
        )

        cook_time = (
            form.cook_time_minutes.data
            or 0
        )

        total_time = (
            prep_time
            + cook_time
        )

        if (
            form.prep_time_minutes.data
            is None
            and form.cook_time_minutes.data
            is None
        ):
            total_time = None

        recipe = Recipe(
            household_id=household_id,
            title=(
                form.title.data
                .strip()
            ),
            difficulty=(
                form.difficulty.data
                or None
            ),
            servings=(
                form.servings.data
            ),
            prep_time_minutes=(
                form.prep_time_minutes.data
            ),
            cook_time_minutes=(
                form.cook_time_minutes.data
            ),
            total_time_minutes=(
                total_time
            ),
            instructions_text=(
                form.instructions_text.data.strip()
                if form.instructions_text.data
                else None
            ),
            source_type="manual",
            is_active=True,
        )

        selected_tag_ids = (
            get_selected_tag_ids()
        )

        recipe.tags = [
            tag
            for tag in available_tags
            if tag.id in selected_tag_ids
        ]

        db.session.add(
            recipe
        )

        db.session.flush()

        ingredient_rows = (
            get_recipe_ingredient_rows()
        )

        for sort_order, row in enumerate(
            ingredient_rows,
            start=10,
        ):
            db.session.add(
                RecipeIngredient(
                    recipe_id=recipe.id,
                    ingredient_id=(
                        row["ingredient_id"]
                    ),
                    original_name=(
                        row["original_name"]
                    ),
                    quantity=(
                        row["quantity"]
                    ),
                    unit_id=(
                        row["unit_id"]
                    ),
                    unit_text=(
                        row["unit_text"]
                    ),
                    sort_order=sort_order,
                )
            )

        db.session.commit()

        flash(
            translate(
                "recipe_created"
            ),
            "success",
        )

        return redirect(
            url_for(
                "recipes.index"
            )
        )

    return render_template(
        "recipes/recipe_form.html",
        form=form,
        page_title=translate(
            "recipe_new_title"
        ),
        tag_groups=tag_groups,
        selected_tag_ids=set(),
        recipe_ingredient_rows=[],
    )

@bp.route(
    "/<uuid:public_id>/edit",
    methods=[
        "GET",
        "POST",
    ],
)
@login_required
def edit(
    public_id,
):
    recipe = get_recipe_or_404(
        public_id
    )

    form = RecipeForm(
        obj=recipe
    )

    configure_recipe_form(
        form
    )

    active_tags = (
        get_active_recipe_tags()
    )

    available_tags_by_id = {
        tag.id: tag
        for tag in active_tags
    }

    for tag in recipe.tags:
        available_tags_by_id.setdefault(
            tag.id,
            tag,
        )

    available_tags = list(
        available_tags_by_id.values()
    )

    available_tags.sort(
        key=lambda tag: (
            tag.group_name,
            tag.sort_order,
            tag.name.lower(),
            tag.id,
        )
    )

    tag_groups = (
        build_recipe_tag_groups(
            available_tags
        )
    )

    if form.validate_on_submit():
        prep_time = (
            form.prep_time_minutes.data
            or 0
        )

        cook_time = (
            form.cook_time_minutes.data
            or 0
        )

        total_time = (
            prep_time
            + cook_time
        )

        if (
            form.prep_time_minutes.data
            is None
            and form.cook_time_minutes.data
            is None
        ):
            total_time = None

        recipe.title = (
            form.title.data
            .strip()
        )

        recipe.difficulty = (
            form.difficulty.data
            or None
        )

        recipe.servings = (
            form.servings.data
        )

        recipe.prep_time_minutes = (
            form.prep_time_minutes.data
        )

        recipe.cook_time_minutes = (
            form.cook_time_minutes.data
        )

        recipe.total_time_minutes = (
            total_time
        )

        recipe.instructions_text = (
            form.instructions_text.data.strip()
            if form.instructions_text.data
            else None
        )

        selected_tag_ids = (
            get_selected_tag_ids()
        )

        recipe.tags = [
            tag
            for tag in available_tags
            if tag.id in selected_tag_ids
        ]

        for ingredient in list(
            recipe.ingredients
        ):
            db.session.delete(
                ingredient
            )

        db.session.flush()

        ingredient_rows = (
            get_recipe_ingredient_rows()
        )

        for sort_order, row in enumerate(
            ingredient_rows,
            start=10,
        ):
            db.session.add(
                RecipeIngredient(
                    recipe_id=recipe.id,
                    ingredient_id=(
                        row["ingredient_id"]
                    ),
                    original_name=(
                        row["original_name"]
                    ),
                    quantity=(
                        row["quantity"]
                    ),
                    unit_id=(
                        row["unit_id"]
                    ),
                    unit_text=(
                        row["unit_text"]
                    ),
                    sort_order=sort_order,
                )
            )

        db.session.commit()

        flash(
            translate(
                "recipe_updated"
            ),
            "success",
        )

        return redirect(
            url_for(
                "recipes.index"
            )
        )

    selected_tag_ids = {
        tag.id
        for tag in recipe.tags
    }

    recipe_ingredient_rows = [
        {
            "ingredient_id": (
                ingredient.ingredient_id
                or 0
            ),
            "name": (
                ingredient.original_name
            ),
            "quantity": (
                str(ingredient.quantity)
                if ingredient.quantity
                is not None
                else ""
            ),
            "unit_id": (
                ingredient.unit_id
                or 0
            ),
            "unit_text": (
                ingredient.unit_text
                or ""
            ),
        }
        for ingredient in recipe.ingredients
    ]

    return render_template(
        "recipes/recipe_form.html",
        form=form,
        page_title=translate(
            "recipe_edit_title"
        ),
        tag_groups=tag_groups,
        selected_tag_ids=(
            selected_tag_ids
        ),
        recipe_ingredient_rows=(
            recipe_ingredient_rows
        ),
    )

@bp.get(
    "/api/ingredient-search"
)
@login_required
def ingredient_search_api():
    query = (
        request.args.get(
            "q",
            "",
        )
        .strip()
    )

    if len(query) < 2:
        return jsonify(
            results=[]
        )

    ingredients = db.session.scalars(
        select(Ingredient)
        .where(
            Ingredient.is_active.is_(
                True
            )
        )
        .order_by(
            Ingredient.canonical_key,
            Ingredient.id,
        )
    ).all()

    query_normalized = (
        query.lower()
    )

    results = []

    for ingredient in ingredients:
        names = []

        for translation in (
            ingredient.translations
        ):
            if translation.name:
                names.append(
                    translation.name
                )

        names.append(
            ingredient.canonical_key
        )

        matched = any(
            query_normalized
            in name.lower()
            for name in names
        )

        if not matched:
            continue

        display_name = next(
            (
                translation.name
                for translation
                in ingredient.translations
                if translation.language_code
                == (
                    current_user
                    .preferred_language
                    or "hu"
                )
            ),
            None,
        )

        if display_name is None:
            display_name = next(
                (
                    translation.name
                    for translation
                    in ingredient.translations
                    if translation.language_code
                    == "hu"
                ),
                None,
            )

        if display_name is None:
            display_name = (
                ingredient.canonical_key
            )

        results.append(
            {
                "id": ingredient.id,
                "name": display_name,
                "canonical_key": (
                    ingredient.canonical_key
                ),
            }
        )

        if len(results) >= 20:
            break

    return jsonify(
        results=results
    )

@bp.get(
    "/<uuid:public_id>"
)
@login_required
def detail(
    public_id,
):
    membership = (
        get_current_membership()
    )

    recipe = db.session.scalar(
        select(Recipe)
        .where(
            Recipe.public_id
            == public_id,
            Recipe.household_id
            == membership.household_id,
            Recipe.is_active.is_(
                True
            ),
        )
    )

    if recipe is None:
        abort(404)

    available_ingredient_ids = set(
        db.session.scalars(
            select(
                InventoryBatch.ingredient_id
            )
            .where(
                InventoryBatch.household_id
                == membership.household_id,
                InventoryBatch.is_active.is_(
                    True
                ),
                InventoryBatch.quantity > 0,
            )
            .distinct()
        ).all()
    )

    ingredient_rows = []

    for recipe_ingredient in (
        recipe.ingredients
    ):
        is_available = (
            recipe_ingredient.ingredient_id
            is not None
            and recipe_ingredient.ingredient_id
            in available_ingredient_ids
        )

        ingredient_rows.append(
            {
                "item": recipe_ingredient,
                "is_available": (
                    is_available
                ),
            }
        )

    return render_template(
        "recipes/detail.html",
        recipe=recipe,
        ingredient_rows=(
            ingredient_rows
        ),
    )
