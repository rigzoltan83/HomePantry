import unicodedata
import os
from io import BytesIO

from decimal import (
    Decimal,
    InvalidOperation,
)
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
from werkzeug.datastructures import (
    FileStorage,
)
from flask_login import (
    current_user,
    login_required,
)
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.extensions import db
from app.i18n import translate
from app.models import (
    HouseholdMember,
    Ingredient,
    InventoryBatch,
    Recipe,
    RecipeImage,
    RecipeIngredient,
    RecipeTag,
    Unit,
)

from . import bp
from .forms import RecipeForm
from .online_recipes import (
    THEMEALDB_CUISINE_MAP,
    THEMEALDB_DIET_MAP,
    THEMEALDB_FOOD_TYPE_MAP,
    download_themealdb_image,
    get_themealdb_recipe,
    search_themealdb_recipes,
    search_themealdb_recipes_by_ingredients,
)
from .import_normalization import (
    normalize_themealdb_import_ingredients,
)
from .recipe_translation import (
    translate_imported_recipe_to_hungarian,
)
from .recipe_images import (
    delete_recipe_image_file,
    save_recipe_image,
)


def save_recipe_form_images(
    recipe,
    form,
):
    saved_images = []

    image_files = list(
        form.new_images.data
        or []
    )

    camera_image = (
        form.camera_image.data
    )

    if (
        camera_image
        and camera_image.filename
    ):
        image_files.append(
            camera_image
        )

    try:
        for image_file in image_files:
            if (
                image_file is None
                or not image_file.filename
            ):
                continue

            saved_image = (
                save_recipe_image(
                    recipe,
                    image_file,
                )
            )

            if saved_image is not None:
                saved_images.append(
                    saved_image
                )

        return saved_images

    except ValueError:
        for saved_image in saved_images:
            delete_recipe_image_file(
                saved_image
            )

        raise


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

        language = (
            current_user.preferred_language
            or "hu"
        )

        for recipe_ingredient in (
            recipe.ingredients
        ):
            ingredient_name = (
                recipe_ingredient.original_name
            )

            if (
                recipe_ingredient.ingredient
                is not None
            ):
                translated_name = next(
                    (
                        translation.name
                        for translation
                        in (
                            recipe_ingredient
                            .ingredient
                            .translations
                        )
                        if (
                            translation.language_code
                            == language
                            and translation.name
                        )
                    ),
                    None,
                )

                if translated_name:
                    ingredient_name = (
                        translated_name
                    )

            searchable_parts.append(
                ingredient_name
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


@bp.get("/online-search")
@login_required
def online_search():
    query = (
        request.args.get(
            "q",
            "",
        )
        .strip()
    )

    safe_ingredient_terms = (
        get_safe_english_ingredient_terms(
            query
        )
    )

    api_query = (
        get_safe_english_search_query(
            query
        )
    )

    cuisine_key = (
        request.args.get(
            "cuisine",
            "",
        )
        .strip()
    )

    food_type_key = (
        request.args.get(
            "food_type",
            "",
        )
        .strip()
    )

    diet_key = (
        request.args.get(
            "diet",
            "",
        )
        .strip()
    )

    availability_percent = (
        request.args.get(
            "availability",
            type=int,
        )
    )

    if availability_percent not in {
        50,
        75,
        100,
    }:
        availability_percent = None

    results = []
    search_error = None

    household_id = (
        get_current_household_id()
    )

    available_ingredient_ids = (
        get_available_ingredient_ids(
            household_id
        )
    )

    english_ingredient_id_map = (
        get_english_ingredient_id_map()
    )

    canonical_ingredient_id_map = (
        get_ingredient_canonical_id_map()
    )

    if (
        food_type_key
        and diet_key
    ):
        search_error = translate(
            "recipe_online_category_conflict"
        )

    area = (
        THEMEALDB_CUISINE_MAP.get(
            cuisine_key
        )
    )

    category = None

    if food_type_key:
        category = (
            THEMEALDB_FOOD_TYPE_MAP.get(
                food_type_key
            )
        )

    elif diet_key:
        category = (
            THEMEALDB_DIET_MAP.get(
                diet_key
            )
        )

    if (
        len(query) >= 2
        and search_error is None
    ):
        try:
            if safe_ingredient_terms:
                results = (
                    search_themealdb_recipes_by_ingredients(
                        safe_ingredient_terms,
                        area=area,
                        category=category,
                    )
                )

            else:
                results = (
                    search_themealdb_recipes(
                        api_query,
                        area=area,
                        category=category,
                    )
                )

        except RuntimeError:
            search_error = translate(
                "recipe_online_error"
            )

    result_rows = []

    for recipe in results:
        availability = (
            get_online_recipe_availability(
                recipe,
                available_ingredient_ids,
                english_ingredient_id_map,
                canonical_ingredient_id_map,
            )
        )

        if (
            availability_percent
            is not None
            and availability[
                "match_percent"
            ]
            < availability_percent
        ):
            continue

        result_rows.append(
            {
                "recipe": recipe,
                "availability": (
                    availability
                ),
            }
        )

    result_rows.sort(
        key=lambda row: (
            -row[
                "availability"
            ][
                "match_percent"
            ],
            (
                row["recipe"].get(
                    "title"
                )
                or ""
            ).casefold(),
        )
    )

    active_tags = (
        get_active_recipe_tags()
    )

    cuisine_choices = [
        tag
        for tag in active_tags
        if (
            tag.group_name
            == "cuisine"
            and tag.key
            in THEMEALDB_CUISINE_MAP
        )
    ]

    food_type_choices = [
        tag
        for tag in active_tags
        if (
            tag.group_name
            == "food_type"
            and tag.key
            in THEMEALDB_FOOD_TYPE_MAP
        )
    ]

    diet_choices = [
        tag
        for tag in active_tags
        if (
            tag.group_name
            == "diet"
            and tag.key
            in THEMEALDB_DIET_MAP
        )
    ]

    return render_template(
        "recipes/online_search.html",
        api_query=api_query,
        query=query,
        result_rows=result_rows,
        search_error=search_error,
        cuisine_key=cuisine_key,
        food_type_key=food_type_key,
        diet_key=diet_key,
        availability_percent=(
            availability_percent
        ),
        cuisine_choices=cuisine_choices,
        food_type_choices=(
            food_type_choices
        ),
        diet_choices=diet_choices,
    )


def find_exact_english_ingredient(
    name,
):
    normalized_name = (
        str(name or "")
        .strip()
        .casefold()
    )

    if not normalized_name:
        return None

    ingredients = db.session.scalars(
        select(Ingredient)
        .where(
            Ingredient.is_active.is_(
                True
            )
        )
    ).all()

    matches = []

    for ingredient in ingredients:
        english_name = next(
            (
                translation.name
                for translation
                in ingredient.translations
                if (
                    translation.language_code
                    == "en"
                    and translation.name
                )
            ),
            None,
        )

        if (
            english_name
            and english_name
            .strip()
            .casefold()
            == normalized_name
        ):
            matches.append(
                ingredient
            )

    if len(matches) != 1:
        return None

    return matches[0]


ONLINE_RECIPE_SEARCH_ALIASES = {
    # Köznyelvi / általános húsnevek.
    # Ezek csak online keresési aliasok,
    # nem HomePantry ingredient-párosítások.
    "csirke": "chicken",
    "csirkehús": "chicken",

    "marha": "beef",
    "marhahús": "beef",

    "sertés": "pork",
    "sertéshús": "pork",
    "disznóhús": "pork",

    "bárány": "lamb",
    "bárányhús": "lamb",

    # Általános halak.
    "lazac": "salmon",
    "tonhal": "tuna",

    # Köznyelvi zöldség / köret nevek.
    "hagyma": "onion",
    "krumpli": "potato",
    "rizs": "rice",

    # Általános alapanyagok.
    "tojás": "egg",
    "tej": "milk",
    "sajt": "cheese",
    "vaj": "butter",
    "gomba": "mushroom",
    "sonka": "ham",
    "méz": "honey",
    "cukor": "sugar",
    "só": "salt",
    "kenyér": "bread",
}


ONLINE_RECIPE_AVAILABILITY_GROUPS = {
    "chicken": {
        "chicken_breast",
        "chicken_thigh",
        "chicken_drumstick",
        "chicken_wing",
        "whole_chicken",
    },

    "rice": {
        "white_rice",
        "brown_rice",
        "basmati_rice",
        "jasmine_rice",
        "arborio_rice",
    },
}


THEMEALDB_AVAILABILITY_NAME_ALIASES = {
    "sugar": "granulated sugar",

    "parmesan cheese": "parmesan",

    "bay leaves": "bay leaf",

    "spring onions": "spring onion",

    "cumin seeds": "cumin",
    "cumin seed": "cumin",
    "potatoes": "potato",

    "onions": "onion",
    "red onions": "red onion",

    "garlic clove": "garlic",
    "garlic cloves": "garlic",

    "mushrooms": "mushroom",

    "tomatoes": "tomato",
    "lemons": "lemon",
    "limes": "lime",

    "eggs": "egg",
    "carrots": "carrot",
}


THEMEALDB_ALWAYS_AVAILABLE = {
    "water",
    "víz",
}


def get_english_ingredient_id_map():
    ingredients = db.session.scalars(
        select(Ingredient)
        .options(
            selectinload(
                Ingredient.translations
            )
        )
        .where(
            Ingredient.is_active.is_(
                True
            )
        )
    ).all()

    english_name_map = {}
    duplicate_names = set()

    for ingredient in ingredients:
        english_names = {
            translation.name
            .strip()
            .casefold()

            for translation
            in ingredient.translations

            if (
                translation.language_code
                == "en"
                and translation.name
                and translation.name.strip()
            )
        }

        for english_name in english_names:
            if english_name in english_name_map:
                duplicate_names.add(
                    english_name
                )
                continue

            english_name_map[
                english_name
            ] = ingredient.id

    for duplicate_name in duplicate_names:
        english_name_map.pop(
            duplicate_name,
            None,
        )

    return english_name_map


def get_ingredient_canonical_id_map():
    rows = db.session.execute(
        select(
            Ingredient.canonical_key,
            Ingredient.id,
        )
        .where(
            Ingredient.is_active.is_(
                True
            )
        )
    ).all()

    return {
        canonical_key: ingredient_id
        for canonical_key, ingredient_id
        in rows
    }


def get_available_ingredient_ids(
    household_id,
):
    return set(
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


def get_online_recipe_availability(
    recipe,
    available_ingredient_ids,
    english_ingredient_id_map,
    canonical_ingredient_id_map,
):
    recipe_ingredients = (
        recipe.get("ingredients")
        or []
    )

    total_count = len(
        recipe_ingredients
    )

    if total_count == 0:
        return {
            "available_count": 0,
            "total_count": 0,
            "missing_count": 0,
            "match_percent": 0,
        }

    available_count = 0

    for item in recipe_ingredients:
        ingredient_name = (
            str(
                item.get("name")
                or ""
            )
            .strip()
            .casefold()
        )

        if not ingredient_name:
            continue

        normalized_ingredient_name = (
            THEMEALDB_AVAILABILITY_NAME_ALIASES
            .get(
                ingredient_name,
                ingredient_name,
            )
        )

        if (
            normalized_ingredient_name
            in THEMEALDB_ALWAYS_AVAILABLE
        ):
            available_count += 1
            continue

        ingredient_id = (
            english_ingredient_id_map.get(
                normalized_ingredient_name
            )
        )

        if (
            ingredient_id
            is not None
            and ingredient_id
            in available_ingredient_ids
        ):
            available_count += 1
            continue

        group_keys = (
            ONLINE_RECIPE_AVAILABILITY_GROUPS
            .get(
                normalized_ingredient_name
            )
        )

        if not group_keys:
            continue

        group_ingredient_ids = {
            canonical_ingredient_id_map[
                canonical_key
            ]
            for canonical_key
            in group_keys
            if canonical_key
            in canonical_ingredient_id_map
        }

        if (
            group_ingredient_ids
            & available_ingredient_ids
        ):
            available_count += 1

    missing_count = (
        total_count
        - available_count
    )

    match_percent = int(
        round(
            (
                available_count
                / total_count
            )
            * 100
        )
    )

    return {
        "available_count": (
            available_count
        ),
        "total_count": total_count,
        "missing_count": missing_count,
        "match_percent": match_percent,
    }


def get_exact_english_search_term(
    query,
):
    normalized_query = (
        str(query or "")
        .strip()
        .casefold()
    )

    if not normalized_query:
        return None

    alias = (
        ONLINE_RECIPE_SEARCH_ALIASES.get(
            normalized_query
        )
    )

    if alias:
        return alias

    ingredients = db.session.scalars(
        select(Ingredient)
        .where(
            Ingredient.is_active.is_(
                True
            )
        )
    ).all()

    matches = []

    for ingredient in ingredients:
        hungarian_names = {
            translation.name
            .strip()
            .casefold()

            for translation
            in ingredient.translations

            if (
                translation.language_code
                == "hu"
                and translation.name
                and translation.name.strip()
            )
        }

        if (
            normalized_query
            not in hungarian_names
        ):
            continue

        english_names = {
            translation.name.strip()

            for translation
            in ingredient.translations

            if (
                translation.language_code
                == "en"
                and translation.name
                and translation.name.strip()
            )
        }

        if len(english_names) != 1:
            continue

        matches.append(
            next(
                iter(
                    english_names
                )
            )
        )

    if len(matches) != 1:
        return None

    return matches[0]


def get_safe_english_ingredient_terms(
    query,
):
    query = (
        str(query or "")
        .strip()
    )

    if not query:
        return []

    exact_match = (
        get_exact_english_search_term(
            query
        )
    )

    if exact_match:
        return [
            exact_match
        ]

    words = query.split()

    if len(words) <= 1:
        return []

    translated_words = []

    for word in words:
        translated_word = (
            get_exact_english_search_term(
                word
            )
        )

        if not translated_word:
            return []

        translated_words.append(
            translated_word
        )

    return translated_words


def get_safe_english_search_query(
    query,
):
    terms = (
        get_safe_english_ingredient_terms(
            query
        )
    )

    if not terms:
        return (
            str(query or "")
            .strip()
        )

    return " ".join(
        terms
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

    import_provider = (
        request.values.get(
            "import_provider",
            "",
        )
        .strip()
        .lower()
    )

    import_id = (
        request.values.get(
            "import_id",
            "",
        )
        .strip()
    )

    recipe_ingredient_rows = []
    selected_tag_ids = set()

    online_import = (
        import_provider
        == "themealdb"
        and bool(import_id)
    )

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

    imported_recipe = None

    if (
        import_provider
        == "themealdb"
        and import_id
    ):
        try:
            imported_recipe = (
                get_themealdb_recipe(
                    import_id
                )
            )

        except RuntimeError:
            imported_recipe = None

            if not form.is_submitted():
                flash(
                    translate(
                        "recipe_online_error"
                    ),
                    "error",
                )

    if (
        not form.is_submitted()
        and imported_recipe
        is not None
    ):
        online_import = True

        translated_recipe = (
            translate_imported_recipe_to_hungarian(
                imported_recipe
            )
        )

        form.title.data = (
            translated_recipe[
                "title"
            ]
        )

        form.instructions_text.data = (
            translated_recipe[
                "instructions"
            ]
        )

        cuisine_key = next(
            (
                key
                for key, value
                in (
                    THEMEALDB_CUISINE_MAP
                    .items()
                )
                if value
                == imported_recipe[
                    "area"
                ]
            ),
            None,
        )

        food_type_key = next(
            (
                key
                for key, value
                in (
                    THEMEALDB_FOOD_TYPE_MAP
                    .items()
                )
                if value
                == imported_recipe[
                    "category"
                ]
            ),
            None,
        )

        diet_key = next(
            (
                key
                for key, value
                in (
                    THEMEALDB_DIET_MAP
                    .items()
                )
                if value
                == imported_recipe[
                    "category"
                ]
            ),
            None,
        )

        imported_tag_keys = {
            key
            for key in (
                cuisine_key,
                food_type_key,
                diet_key,
            )
            if key
        }

        selected_tag_ids = {
            tag.id
            for tag in available_tags
            if tag.key
            in imported_tag_keys
        }

        recipe_ingredient_rows = (
            normalize_themealdb_import_ingredients(
                imported_recipe
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
            source_type=(
                "themealdb"
                if (
                    import_provider
                    == "themealdb"
                    and import_id
                )
                else "manual"
            ),
            source_id=(
                import_id
                if (
                    import_provider
                    == "themealdb"
                    and import_id
                )
                else None
            ),
            source_url=(
                imported_recipe.get(
                    "source_url"
                )
                if imported_recipe
                is not None
                else None
            ),
            external_data=(
                {
                    "provider": (
                        "themealdb"
                    ),
                    "external_id": (
                        import_id
                    ),
                    "category": (
                        imported_recipe.get(
                            "category"
                        )
                    ),
                    "area": (
                        imported_recipe.get(
                            "area"
                        )
                    ),
                    "image_url": (
                        imported_recipe.get(
                            "image_url"
                        )
                    ),
                    "youtube_url": (
                        imported_recipe.get(
                            "youtube_url"
                        )
                    ),
                }
                if (
                    import_provider
                    == "themealdb"
                    and import_id
                    and imported_recipe
                    is not None
                )
                else (
                    {
                        "provider": (
                            "themealdb"
                        ),
                        "external_id": (
                            import_id
                        ),
                    }
                    if (
                        import_provider
                        == "themealdb"
                        and import_id
                    )
                    else None
                )
            ),
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

        saved_images = []

        try:
            saved_images = (
                save_recipe_form_images(
                    recipe,
                    form,
                )
            )

        except ValueError:
            db.session.rollback()

            for saved_image in saved_images:
                delete_recipe_image_file(
                    saved_image
                )

            flash(
                translate(
                    "recipe_image_invalid"
                ),
                "error",
            )

            return render_template(
                "recipes/recipe_form.html",
                form=form,
                page_title=translate(
                    "recipe_new_title"
                ),
                tag_groups=tag_groups,
                selected_tag_ids=(
                    selected_tag_ids
                ),
                recipe_ingredient_rows=(
                    ingredient_rows
                ),
                online_import=(
                    online_import
                ),
            )

        has_uploaded_recipe_image = (
            len(saved_images) > 0
        )

        if has_uploaded_recipe_image:
            for index, image in enumerate(
                saved_images
            ):
                image.is_cover = (
                    index == 0
                )

        import_source_image = (
            request.form.get(
                "import_source_image"
            )
            == "1"
        )

        if (
            import_source_image
            and import_provider
            == "themealdb"
            and imported_recipe
            is not None
            and imported_recipe.get(
                "image_url"
            )
        ):
            try:
                image_data = (
                    download_themealdb_image(
                        imported_recipe[
                            "image_url"
                        ]
                    )
                )

                remote_image = FileStorage(
                    stream=BytesIO(
                        image_data
                    ),
                    filename=(
                        "themealdb-"
                        f"{import_id}.jpg"
                    ),
                    content_type=(
                        "image/jpeg"
                    ),
                )

                saved_image = (
                    save_recipe_image(
                        recipe,
                        remote_image,
                    )
                )

                if saved_image is not None:

                    if (
                        has_uploaded_recipe_image
                    ):
                        saved_image.is_cover = (
                            False
                        )

                    saved_images.append(
                        saved_image
                    )

            except (
                RuntimeError,
                ValueError,
                OSError,
            ):
                flash(
                    translate(
                        "recipe_online_import_image_error"
                    ),
                    "warning",
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
        selected_tag_ids=(
            selected_tag_ids
        ),
        recipe_ingredient_rows=(
            recipe_ingredient_rows
        ),
        online_import=online_import,
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

        saved_images = []

        try:
            saved_images = (
                save_recipe_form_images(
                    recipe,
                    form,
                )
            )

            db.session.commit()

        except ValueError:
            db.session.rollback()

            for saved_image in saved_images:
                delete_recipe_image_file(
                    saved_image
                )

            flash(
                translate(
                    "recipe_image_invalid"
                ),
                "error",
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
                        str(
                            ingredient.quantity
                        )
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
                for ingredient
                in recipe.ingredients
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
                recipe=recipe,
            )

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
        recipe=recipe,
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

    language = (
        current_user.preferred_language
        or "hu"
    )

    results = []

    for ingredient in ingredients:
        display_name = next(
            (
                translation.name
                for translation
                in ingredient.translations
                if (
                    translation.language_code
                    == language
                    and translation.name
                )
            ),
            None,
        )

        if display_name is None:
            continue

        matched = (
            query_normalized
            in display_name.lower()
        )

        if not matched:
            continue

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


def format_recipe_quantity(
    value,
):
    if value is None:
        return ""

    try:
        number = float(value)
    except (
        TypeError,
        ValueError,
    ):
        return str(value)

    whole = int(number)
    fraction = number - whole

    fractions = [
        (1 / 8, "1/8"),
        (1 / 4, "1/4"),
        (1 / 3, "1/3"),
        (3 / 8, "3/8"),
        (1 / 2, "1/2"),
        (5 / 8, "5/8"),
        (2 / 3, "2/3"),
        (3 / 4, "3/4"),
        (7 / 8, "7/8"),
    ]

    best_fraction = None
    best_difference = None

    for fraction_value, label in fractions:
        difference = abs(
            fraction - fraction_value
        )

        if (
            best_difference is None
            or difference < best_difference
        ):
            best_difference = difference
            best_fraction = label

    if (
        best_difference is not None
        and best_difference <= 0.01
    ):
        if whole:
            return (
                f"{whole} "
                f"{best_fraction}"
            )

        return best_fraction

    if abs(
        number - round(number)
    ) <= 0.000001:
        return str(
            int(
                round(number)
            )
        )

    text = f"{number:.3f}"

    return (
        text
        .rstrip("0")
        .rstrip(".")
    )


def get_recipe_unit_display(
    unit,
):
    if unit is None:
        return ""

    compact_unit_codes = {
        "mg",
        "g",
        "kg",
        "ml",
        "cl",
        "dl",
        "l",
    }

    if unit.code in compact_unit_codes:
        return (
            unit.symbol
            or unit.code
        )

    preferred_language = (
        current_user.preferred_language
        or "hu"
    )

    unit_name = next(
        (
            translation.name
            for translation
            in unit.translations
            if (
                translation.language_code
                == preferred_language
                and translation.name
            )
        ),
        None,
    )

    if unit_name is None:
        unit_name = next(
            (
                translation.name
                for translation
                in unit.translations
                if (
                    translation.language_code
                    == "hu"
                    and translation.name
                )
            ),
            None,
        )

    return (
        unit_name
        or unit.symbol
        or unit.code
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

    cover_image = next(
        (
            image
            for image in recipe.images
            if image.is_cover
        ),
        None,
    )

    if (
        cover_image is None
        and recipe.images
    ):
        cover_image = (
            recipe.images[0]
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
                "quantity_display": (
                    format_recipe_quantity(
                        recipe_ingredient.quantity
                    )
                ),
                "unit_display": (
                    get_recipe_unit_display(
                        recipe_ingredient.unit
                    )
                ),
            }
        )

    return render_template(
        "recipes/detail.html",
        recipe=recipe,
        ingredient_rows=(
            ingredient_rows
        ),
        cover_image=cover_image,
    )

@bp.get(
    "/recipe-images/<uuid:public_id>"
)
@login_required
def recipe_image(
    public_id,
):
    household_id = (
        get_current_household_id()
    )

    image = db.session.scalar(
        select(RecipeImage)
        .join(
            Recipe,
            Recipe.id
            == RecipeImage.recipe_id,
        )
        .where(
            RecipeImage.public_id
            == public_id,
            Recipe.household_id
            == household_id,
        )
    )

    if image is None:
        abort(404)

    image_root = (
        current_app.config[
            "RECIPE_IMAGE_UPLOAD_DIR"
        ]
    )

    directory = os.path.join(
        image_root,
        str(image.recipe.public_id),
    )

    return send_from_directory(
        directory,
        image.stored_filename,
        mimetype="image/webp",
        max_age=86400,
    )


@bp.post(
    "/<uuid:recipe_public_id>/images/"
    "<uuid:image_public_id>/cover"
)
@login_required
def recipe_image_cover(
    recipe_public_id,
    image_public_id,
):
    recipe = get_recipe_or_404(
        recipe_public_id
    )

    image = db.session.scalar(
        select(RecipeImage)
        .where(
            RecipeImage.public_id
            == image_public_id,
            RecipeImage.recipe_id
            == recipe.id,
        )
    )

    if image is None:
        abort(404)

    for recipe_image in recipe.images:
        recipe_image.is_cover = (
            recipe_image.id
            == image.id
        )

    db.session.commit()

    flash(
        translate(
            "recipe_image_cover_updated"
        ),
        "success",
    )

    return redirect(
        url_for(
            "recipes.edit",
            public_id=recipe.public_id,
        )
    )


@bp.post(
    "/<uuid:recipe_public_id>/images/"
    "<uuid:image_public_id>/delete"
)
@login_required
def recipe_image_delete(
    recipe_public_id,
    image_public_id,
):
    recipe = get_recipe_or_404(
        recipe_public_id
    )

    image = db.session.scalar(
        select(RecipeImage)
        .where(
            RecipeImage.public_id
            == image_public_id,
            RecipeImage.recipe_id
            == recipe.id,
        )
    )

    if image is None:
        abort(404)

    was_cover = image.is_cover

    delete_recipe_image_file(
        image
    )

    db.session.delete(
        image
    )

    db.session.flush()

    if was_cover:
        next_image = db.session.scalar(
            select(RecipeImage)
            .where(
                RecipeImage.recipe_id
                == recipe.id,
                RecipeImage.id
                != image.id,
            )
            .order_by(
                RecipeImage.sort_order,
                RecipeImage.id,
            )
            .limit(1)
        )

        if next_image is not None:
            next_image.is_cover = True

    db.session.commit()

    flash(
        translate(
            "recipe_image_deleted"
        ),
        "success",
    )

    return redirect(
        url_for(
            "recipes.edit",
            public_id=recipe.public_id,
        )
    )

@bp.post(
    "/<uuid:public_id>/delete"
)
@login_required
def delete(
    public_id,
):
    recipe = get_recipe_or_404(
        public_id
    )

    recipe.is_active = False

    db.session.commit()

    flash(
        translate(
            "recipe_deleted"
        ),
        "success",
    )

    return redirect(
        url_for(
            "recipes.index"
        )
    )
