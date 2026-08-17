from pathlib import Path
import sys

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT),
    )

load_dotenv(
    PROJECT_ROOT / ".env"
)


from app import create_app
from app.extensions import db
from app.models import (
    Ingredient,
    IngredientUnit,
    Unit,
)


MASS_UNITS = [
    "g",
    "kg",
    "oz",
    "lb",
]

VOLUME_UNITS = [
    "ml",
    "cl",
    "dl",
    "l",
    "tsp",
    "tbsp",
    "cup_metric",
    "tsp_us",
    "tbsp_us",
    "fl_oz_us",
    "cup_us",
    "pint_us",
    "quart_us",
    "gallon_us",
    "fl_oz_imp",
    "pint_imp",
    "quart_imp",
    "gallon_imp",
]

COUNT_UNITS = [
    "pc",
    "dozen",
]

MASS_AND_COUNT = [
    "g",
    "kg",
    "oz",
    "lb",
    "pc",
]

INGREDIENT_OVERRIDES = {
    "egg": COUNT_UNITS,

    "milk": VOLUME_UNITS,
    "lactose_free_milk": VOLUME_UNITS,
    "cream": VOLUME_UNITS,

    "sunflower_oil": VOLUME_UNITS,
    "olive_oil": VOLUME_UNITS,
    "vanilla_extract": VOLUME_UNITS,
    "soy_sauce": VOLUME_UNITS,
    "worcestershire_sauce": VOLUME_UNITS,
    "vinegar": VOLUME_UNITS,
    "balsamic_vinegar": VOLUME_UNITS,
    "passata": VOLUME_UNITS,

    "tomato": MASS_AND_COUNT,
    "onion": MASS_AND_COUNT,
    "red_onion": MASS_AND_COUNT,
    "garlic": MASS_AND_COUNT,
    "carrot": MASS_AND_COUNT,
    "potato": MASS_AND_COUNT,
    "sweet_potato": MASS_AND_COUNT,
    "apple": MASS_AND_COUNT,
    "pear": MASS_AND_COUNT,
    "banana": MASS_AND_COUNT,
    "orange": MASS_AND_COUNT,
    "lemon": MASS_AND_COUNT,
    "lime": MASS_AND_COUNT,
    "bell_pepper": MASS_AND_COUNT,
    "chili_pepper": MASS_AND_COUNT,
    "cucumber": MASS_AND_COUNT,
    "zucchini": MASS_AND_COUNT,
    "eggplant": MASS_AND_COUNT,
}


def get_unit(code):
    unit = (
        db.session.query(Unit)
        .filter_by(code=code)
        .one_or_none()
    )

    if unit is None:
        raise RuntimeError(
            f"Missing unit: {code}"
        )

    return unit


def seed_ingredient_units():
    ingredients = (
        db.session.query(Ingredient)
        .filter(
            Ingredient.is_active.is_(True)
        )
        .all()
    )

    unit_cache = {}

    def cached_unit(code):
        if code not in unit_cache:
            unit_cache[code] = get_unit(
                code
            )

        return unit_cache[code]

    for ingredient in ingredients:
        if (
            ingredient.canonical_key
            in INGREDIENT_OVERRIDES
        ):
            allowed_codes = (
                INGREDIENT_OVERRIDES[
                    ingredient.canonical_key
                ]
            )
        elif (
            ingredient.default_unit
            is not None
            and ingredient.default_unit.dimension
            == "volume"
        ):
            allowed_codes = VOLUME_UNITS
        elif (
            ingredient.default_unit
            is not None
            and ingredient.default_unit.dimension
            == "count"
        ):
            allowed_codes = COUNT_UNITS
        else:
            allowed_codes = MASS_UNITS

        desired_unit_ids = set()

        for sort_order, code in enumerate(
            allowed_codes,
            start=10,
        ):
            unit = cached_unit(code)

            desired_unit_ids.add(
                unit.id
            )

            mapping = (
                db.session.query(
                    IngredientUnit
                )
                .filter_by(
                    ingredient_id=ingredient.id,
                    unit_id=unit.id,
                )
                .one_or_none()
            )

            if mapping is None:
                mapping = IngredientUnit(
                    ingredient=ingredient,
                    unit=unit,
                )

                db.session.add(mapping)

            mapping.sort_order = (
                sort_order
            )

            mapping.is_default = (
                ingredient.default_unit_id
                == unit.id
            )

        for mapping in list(
            ingredient.allowed_units
        ):
            if (
                mapping.unit_id
                not in desired_unit_ids
            ):
                db.session.delete(
                    mapping
                )

    db.session.commit()


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        seed_ingredient_units()

        print(
            "Ingredient unit mappings seeded."
        )
