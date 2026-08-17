from decimal import Decimal
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
    Unit,
    UnitTranslation,
)


UNITS = [
    # -------------------------------------------------
    # MASS
    # Base unit: gram
    # -------------------------------------------------
    {
        "code": "mg",
        "dimension": "mass",
        "system": "metric",
        "symbol": "mg",
        "factor": "0.001",
        "sort_order": 10,
        "hu": "milligramm",
        "en": "milligram",
    },
    {
        "code": "g",
        "dimension": "mass",
        "system": "metric",
        "symbol": "g",
        "factor": "1",
        "sort_order": 20,
        "hu": "gramm",
        "en": "gram",
    },
    {
        "code": "kg",
        "dimension": "mass",
        "system": "metric",
        "symbol": "kg",
        "factor": "1000",
        "sort_order": 30,
        "hu": "kilogramm",
        "en": "kilogram",
    },
    {
        "code": "oz",
        "dimension": "mass",
        "system": "us_customary",
        "symbol": "oz",
        "factor": "28.349523125",
        "sort_order": 40,
        "hu": "uncia",
        "en": "ounce",
    },
    {
        "code": "lb",
        "dimension": "mass",
        "system": "us_customary",
        "symbol": "lb",
        "factor": "453.59237",
        "sort_order": 50,
        "hu": "font",
        "en": "pound",
    },

    # -------------------------------------------------
    # VOLUME
    # Base unit: millilitre
    # -------------------------------------------------
    {
        "code": "ml",
        "dimension": "volume",
        "system": "metric",
        "symbol": "ml",
        "factor": "1",
        "sort_order": 100,
        "hu": "milliliter",
        "en": "millilitre",
    },
    {
        "code": "cl",
        "dimension": "volume",
        "system": "metric",
        "symbol": "cl",
        "factor": "10",
        "sort_order": 110,
        "hu": "centiliter",
        "en": "centilitre",
    },
    {
        "code": "dl",
        "dimension": "volume",
        "system": "metric",
        "symbol": "dl",
        "factor": "100",
        "sort_order": 120,
        "hu": "deciliter",
        "en": "decilitre",
    },
    {
        "code": "l",
        "dimension": "volume",
        "system": "metric",
        "symbol": "l",
        "factor": "1000",
        "sort_order": 130,
        "hu": "liter",
        "en": "litre",
    },

    # Generic recipe measures.
    #
    # These are deliberately normalized recipe units,
    # not historical UK/US legal-volume definitions.
    {
        "code": "tsp",
        "dimension": "volume",
        "system": "universal",
        "symbol": "tsp",
        "factor": "5",
        "sort_order": 200,
        "hu": "teáskanál",
        "en": "teaspoon",
    },
    {
        "code": "tbsp",
        "dimension": "volume",
        "system": "universal",
        "symbol": "tbsp",
        "factor": "15",
        "sort_order": 210,
        "hu": "evőkanál",
        "en": "tablespoon",
    },
    {
        "code": "cup_metric",
        "dimension": "volume",
        "system": "metric",
        "symbol": "cup",
        "factor": "250",
        "sort_order": 220,
        "hu": "metrikus csésze",
        "en": "metric cup",
    },

    # -------------------------------------------------
    # US CUSTOMARY VOLUME
    # -------------------------------------------------
    {
        "code": "tsp_us",
        "dimension": "volume",
        "system": "us_customary",
        "symbol": "tsp",
        "factor": "4.92892159375",
        "sort_order": 300,
        "hu": "amerikai teáskanál",
        "en": "US teaspoon",
    },
    {
        "code": "tbsp_us",
        "dimension": "volume",
        "system": "us_customary",
        "symbol": "tbsp",
        "factor": "14.78676478125",
        "sort_order": 310,
        "hu": "amerikai evőkanál",
        "en": "US tablespoon",
    },
    {
        "code": "fl_oz_us",
        "dimension": "volume",
        "system": "us_customary",
        "symbol": "fl oz",
        "factor": "29.5735295625",
        "sort_order": 320,
        "hu": "amerikai folyadékuncia",
        "en": "US fluid ounce",
    },
    {
        "code": "cup_us",
        "dimension": "volume",
        "system": "us_customary",
        "symbol": "cup",
        "factor": "236.5882365",
        "sort_order": 330,
        "hu": "amerikai csésze",
        "en": "US cup",
    },
    {
        "code": "pint_us",
        "dimension": "volume",
        "system": "us_customary",
        "symbol": "pt",
        "factor": "473.176473",
        "sort_order": 340,
        "hu": "amerikai pint",
        "en": "US pint",
    },
    {
        "code": "quart_us",
        "dimension": "volume",
        "system": "us_customary",
        "symbol": "qt",
        "factor": "946.352946",
        "sort_order": 350,
        "hu": "amerikai quart",
        "en": "US quart",
    },
    {
        "code": "gallon_us",
        "dimension": "volume",
        "system": "us_customary",
        "symbol": "gal",
        "factor": "3785.411784",
        "sort_order": 360,
        "hu": "amerikai gallon",
        "en": "US gallon",
    },

    # -------------------------------------------------
    # UK IMPERIAL VOLUME
    # -------------------------------------------------
    {
        "code": "fl_oz_imp",
        "dimension": "volume",
        "system": "imperial",
        "symbol": "fl oz",
        "factor": "28.4130625",
        "sort_order": 400,
        "hu": "birodalmi folyadékuncia",
        "en": "imperial fluid ounce",
    },
    {
        "code": "pint_imp",
        "dimension": "volume",
        "system": "imperial",
        "symbol": "pt",
        "factor": "568.26125",
        "sort_order": 410,
        "hu": "birodalmi pint",
        "en": "imperial pint",
    },
    {
        "code": "quart_imp",
        "dimension": "volume",
        "system": "imperial",
        "symbol": "qt",
        "factor": "1136.5225",
        "sort_order": 420,
        "hu": "birodalmi quart",
        "en": "imperial quart",
    },
    {
        "code": "gallon_imp",
        "dimension": "volume",
        "system": "imperial",
        "symbol": "gal",
        "factor": "4546.09",
        "sort_order": 430,
        "hu": "birodalmi gallon",
        "en": "imperial gallon",
    },

    # -------------------------------------------------
    # COUNT
    # Base unit: piece
    # -------------------------------------------------
    {
        "code": "pc",
        "dimension": "count",
        "system": "universal",
        "symbol": "db",
        "factor": "1",
        "sort_order": 500,
        "hu": "darab",
        "en": "piece",
    },
    {
        "code": "pair",
        "dimension": "count",
        "system": "universal",
        "symbol": "pár",
        "factor": "2",
        "sort_order": 510,
        "hu": "pár",
        "en": "pair",
    },
    {
        "code": "dozen",
        "dimension": "count",
        "system": "universal",
        "symbol": "doz",
        "factor": "12",
        "sort_order": 520,
        "hu": "tucat",
        "en": "dozen",
    },
]


def upsert_translation(
    unit,
    language_code,
    name,
):
    translation = next(
        (
            item
            for item in unit.translations
            if item.language_code
            == language_code
        ),
        None,
    )

    if translation is None:
        translation = UnitTranslation(
            language_code=language_code,
            name=name,
        )

        unit.translations.append(
            translation
        )

    else:
        translation.name = name


def seed_units():
    for item in UNITS:
        unit = (
            db.session.query(Unit)
            .filter_by(
                code=item["code"]
            )
            .one_or_none()
        )

        if unit is None:
            unit = Unit(
                code=item["code"]
            )

            db.session.add(unit)

        unit.dimension = (
            item["dimension"]
        )

        unit.system = (
            item["system"]
        )

        unit.symbol = (
            item["symbol"]
        )

        unit.factor_to_base = Decimal(
            item["factor"]
        )

        unit.sort_order = (
            item["sort_order"]
        )

        unit.is_active = True

        upsert_translation(
            unit,
            "hu",
            item["hu"],
        )

        upsert_translation(
            unit,
            "en",
            item["en"],
        )

    db.session.commit()


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        seed_units()

        print(
            f"Seeded {len(UNITS)} units."
        )
