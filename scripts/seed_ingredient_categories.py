import os
from pathlib import Path
import sys

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT),
    )

if not os.getenv("DATABASE_URL"):
    env_file = PROJECT_ROOT / ".env"
    if env_file.is_file():
        load_dotenv(env_file)


from app import create_app
from app.extensions import db
from app.models import (
    IngredientCategory,
    IngredientCategoryTranslation,
)


CATEGORIES = [
    {
        "key": "food",
        "parent": None,
        "sort_order": 10,
        "hu": "Élelmiszer",
        "en": "Food",
    },

    {
        "key": "meat",
        "parent": "food",
        "sort_order": 100,
        "hu": "Hús",
        "en": "Meat",
    },
    {
        "key": "poultry",
        "parent": "meat",
        "sort_order": 110,
        "hu": "Szárnyas",
        "en": "Poultry",
    },
    {
        "key": "pork",
        "parent": "meat",
        "sort_order": 120,
        "hu": "Sertéshús",
        "en": "Pork",
    },
    {
        "key": "beef",
        "parent": "meat",
        "sort_order": 130,
        "hu": "Marhahús",
        "en": "Beef",
    },
    {
        "key": "other_meat",
        "parent": "meat",
        "sort_order": 140,
        "hu": "Egyéb hús",
        "en": "Other meat",
    },

    {
        "key": "fish_and_seafood",
        "parent": "food",
        "sort_order": 200,
        "hu": "Hal és tengeri étel",
        "en": "Fish and seafood",
    },

    {
        "key": "dairy",
        "parent": "food",
        "sort_order": 300,
        "hu": "Tejtermék",
        "en": "Dairy",
    },
    {
        "key": "milk",
        "parent": "dairy",
        "sort_order": 310,
        "hu": "Tej",
        "en": "Milk",
    },
    {
        "key": "cheese",
        "parent": "dairy",
        "sort_order": 320,
        "hu": "Sajt",
        "en": "Cheese",
    },
    {
        "key": "yogurt",
        "parent": "dairy",
        "sort_order": 330,
        "hu": "Joghurt",
        "en": "Yogurt",
    },
    {
        "key": "cream_and_sour_cream",
        "parent": "dairy",
        "sort_order": 340,
        "hu": "Tejszín és tejföl",
        "en": "Cream and sour cream",
    },
    {
        "key": "butter_and_spreads",
        "parent": "dairy",
        "sort_order": 350,
        "hu": "Vaj és kenhető tejtermék",
        "en": "Butter and dairy spreads",
    },

    {
        "key": "eggs",
        "parent": "food",
        "sort_order": 400,
        "hu": "Tojás",
        "en": "Eggs",
    },

    {
        "key": "flour_and_milling",
        "parent": "food",
        "sort_order": 500,
        "hu": "Liszt és őrlemény",
        "en": "Flour and milling products",
    },
    {
        "key": "wheat_flour",
        "parent": "flour_and_milling",
        "sort_order": 510,
        "hu": "Búzaliszt",
        "en": "Wheat flour",
    },
    {
        "key": "specialty_flour",
        "parent": "flour_and_milling",
        "sort_order": 520,
        "hu": "Speciális liszt",
        "en": "Specialty flour",
    },
    {
        "key": "meal_and_semolina",
        "parent": "flour_and_milling",
        "sort_order": 530,
        "hu": "Dara és őrlemény",
        "en": "Meal and semolina",
    },

    {
        "key": "pasta",
        "parent": "food",
        "sort_order": 600,
        "hu": "Tészta",
        "en": "Pasta",
    },

    {
        "key": "rice_and_grains",
        "parent": "food",
        "sort_order": 700,
        "hu": "Rizs és gabona",
        "en": "Rice and grains",
    },
    {
        "key": "rice",
        "parent": "rice_and_grains",
        "sort_order": 710,
        "hu": "Rizs",
        "en": "Rice",
    },
    {
        "key": "grains",
        "parent": "rice_and_grains",
        "sort_order": 720,
        "hu": "Gabona",
        "en": "Grains",
    },

    {
        "key": "legumes",
        "parent": "food",
        "sort_order": 800,
        "hu": "Hüvelyes",
        "en": "Legumes",
    },

    {
        "key": "vegetables",
        "parent": "food",
        "sort_order": 900,
        "hu": "Zöldség",
        "en": "Vegetables",
    },

    {
        "key": "fruit",
        "parent": "food",
        "sort_order": 1000,
        "hu": "Gyümölcs",
        "en": "Fruit",
    },

    {
        "key": "herbs_and_spices",
        "parent": "food",
        "sort_order": 1100,
        "hu": "Fűszer és zöldfűszer",
        "en": "Herbs and spices",
    },
    {
        "key": "spices",
        "parent": "herbs_and_spices",
        "sort_order": 1110,
        "hu": "Fűszer",
        "en": "Spices",
    },
    {
        "key": "herbs",
        "parent": "herbs_and_spices",
        "sort_order": 1120,
        "hu": "Zöldfűszer",
        "en": "Herbs",
    },

    {
        "key": "oils_and_fats",
        "parent": "food",
        "sort_order": 1200,
        "hu": "Olaj és zsiradék",
        "en": "Oils and fats",
    },

    {
        "key": "sauces_and_condiments",
        "parent": "food",
        "sort_order": 1300,
        "hu": "Szósz és ízesítő",
        "en": "Sauces and condiments",
    },

    {
        "key": "baking",
        "parent": "food",
        "sort_order": 1400,
        "hu": "Sütési alapanyag",
        "en": "Baking ingredients",
    },

    {
        "key": "sugar_and_sweeteners",
        "parent": "food",
        "sort_order": 1500,
        "hu": "Cukor és édesítőszer",
        "en": "Sugar and sweeteners",
    },

    {
        "key": "nuts_and_seeds",
        "parent": "food",
        "sort_order": 1600,
        "hu": "Diófélék és magvak",
        "en": "Nuts and seeds",
    },

    {
        "key": "canned_and_preserved",
        "parent": "food",
        "sort_order": 1700,
        "hu": "Konzerv és tartósított étel",
        "en": "Canned and preserved food",
    },

    {
        "key": "frozen",
        "parent": "food",
        "sort_order": 1800,
        "hu": "Fagyasztott élelmiszer",
        "en": "Frozen food",
    },

    {
        "key": "bread_and_bakery",
        "parent": "food",
        "sort_order": 1900,
        "hu": "Kenyér és pékáru",
        "en": "Bread and bakery",
    },

    {
        "key": "drinks",
        "parent": "food",
        "sort_order": 2000,
        "hu": "Ital",
        "en": "Drinks",
    },
    {
        "key": "non_alcoholic_drinks",
        "parent": "drinks",
        "sort_order": 2010,
        "hu": "Alkoholmentes ital",
        "en": "Non-alcoholic drinks",
    },

    {
        "key": "prepared_food",
        "parent": "food",
        "sort_order": 2100,
        "hu": "Készétel",
        "en": "Prepared food",
    },

    {
        "key": "other_food",
        "parent": "food",
        "sort_order": 9999,
        "hu": "Egyéb élelmiszer",
        "en": "Other food",
    },
]


def upsert_translation(
    category,
    language_code,
    name,
):
    translation = next(
        (
            item
            for item in category.translations
            if item.language_code
            == language_code
        ),
        None,
    )

    if translation is None:
        translation = (
            IngredientCategoryTranslation(
                language_code=language_code,
                name=name,
            )
        )

        category.translations.append(
            translation
        )

    else:
        translation.name = name


def seed_categories():
    categories_by_key = {}

    for item in CATEGORIES:
        category = (
            db.session.query(
                IngredientCategory
            )
            .filter_by(
                canonical_key=item["key"]
            )
            .one_or_none()
        )

        if category is None:
            category = IngredientCategory(
                canonical_key=item["key"]
            )

            db.session.add(category)

        category.sort_order = (
            item["sort_order"]
        )

        category.is_active = True

        upsert_translation(
            category,
            "hu",
            item["hu"],
        )

        upsert_translation(
            category,
            "en",
            item["en"],
        )

        categories_by_key[
            item["key"]
        ] = category

    db.session.flush()

    for item in CATEGORIES:
        category = categories_by_key[
            item["key"]
        ]

        parent_key = item["parent"]

        if parent_key is None:
            category.parent = None
        else:
            category.parent = (
                categories_by_key[
                    parent_key
                ]
            )

    db.session.commit()


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        seed_categories()

        print(
            f"Seeded {len(CATEGORIES)} "
            "ingredient categories."
        )
