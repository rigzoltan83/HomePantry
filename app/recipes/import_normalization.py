import re
from decimal import (
    Decimal,
    InvalidOperation,
    ROUND_HALF_UP,
)

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.extensions import db
from app.models import (
    Ingredient,
    Unit,
)


THEMEALDB_IMPORT_INGREDIENT_ALIASES = {
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

    "parmesan cheese": "parmesan",

    "sugar": "granulated sugar",

    "cumin seeds": "cumin",
    "cumin seed": "cumin",
}


THEMEALDB_FALLBACK_HU_NAMES = {
    "chicken": "csirke",
    "rice": "rizs",
    "water": "víz",
    "ginger": "gyömbér",
    "oil": "olaj",
    "pepper": "bors",
    "red pepper": "piros paprika",
    "green pepper": "zöld paprika",
    "coriander": "koriander",
    "raisins": "mazsola",
    "spring onions": "újhagyma",
    "coconut milk": "kókusztej",
    "plain flour": "finomliszt",
    "flour": "liszt",
    "bay leaf": "babérlevél",
    "bay leaves": "babérlevél",
    "green olives": "zöld olívabogyó",
    "black olives": "fekete olívabogyó",
    "tomato puree": "paradicsompüré",
    "chicken stock": "csirkealaplé",
    "chicken stock cube": (
        "csirkehúsleveskocka"
    ),
    "potato starch": "burgonyakeményítő",
    "garlic powder": "fokhagymapor",
    "onion salt": "hagymás só",
    "ginger paste": "gyömbérpaszta",
    "fish sauce": "halszósz",
}


THEMEALDB_UNIT_ALIASES = {
    "mg": "mg",
    "milligram": "mg",
    "milligrams": "mg",

    "g": "g",
    "gram": "g",
    "grams": "g",

    "kg": "kg",
    "kilogram": "kg",
    "kilograms": "kg",

    "oz": "oz",
    "ounce": "oz",
    "ounces": "oz",

    "lb": "lb",
    "lbs": "lb",
    "pound": "lb",
    "pounds": "lb",

    "ml": "ml",
    "milliliter": "ml",
    "milliliters": "ml",
    "millilitre": "ml",
    "millilitres": "ml",

    "cl": "cl",
    "dl": "dl",

    "l": "l",
    "liter": "l",
    "liters": "l",
    "litre": "l",
    "litres": "l",

    "tsp": "tsp",
    "teaspoon": "tsp",
    "teaspoons": "tsp",

    "tbsp": "tbsp",
    "tablespoon": "tbsp",
    "tablespoons": "tbsp",

    "fl oz": "fl_oz_us",
    "fluid ounce": "fl_oz_us",
    "fluid ounces": "fl_oz_us",

    "pint": "pint_us",
    "pints": "pint_us",

    "quart": "quart_us",
    "quarts": "quart_us",

    "gallon": "gallon_us",
    "gallons": "gallon_us",

    "piece": "pc",
    "pieces": "pc",
    "pc": "pc",
    "pcs": "pc",

    "dozen": "dozen",
}


THEMEALDB_HU_UNIT_TEXT = {
    "clove": "gerezd",
    "cloves": "gerezd",

    "cup": "csésze",
    "cups": "csésze",

    "slice": "szelet",
    "slices": "szelet",

    "pinch": "csipet",
    "pinches": "csipet",

    "handful": "marék",
    "handfuls": "marék",

    "bunch": "csokor",
    "bunches": "csokor",

    "sprig": "ág",
    "sprigs": "ág",

    "can": "konzerv",
    "cans": "konzerv",

    "tin": "konzerv",
    "tins": "konzerv",

    "packet": "csomag",
    "packets": "csomag",

    "package": "csomag",
    "packages": "csomag",

    "to taste": "ízlés szerint",
    "as needed": "szükség szerint",
}


THEMEALDB_UNIT_DISPLAY_TEXT = {
    "mg": "mg",
    "g": "g",
    "kg": "kg",

    "oz": "uncia",
    "lb": "font",

    "ml": "ml",
    "cl": "cl",
    "dl": "dl",
    "l": "l",

    "tsp": "teáskanál",
    "tsp_us": "teáskanál",

    "tbsp": "evőkanál",
    "tbsp_us": "evőkanál",

    "cup_metric": "csésze",
    "cup_us": "csésze",

    "fl_oz_us": "folyadékuncia",
    "fl_oz_imp": "folyadékuncia",

    "pc": "db",
    "pair": "pár",
    "dozen": "tucat",
}


THEMEALDB_MEASURE_NOTE_TRANSLATIONS = {
    "boneless skin": (
        "csont és bőr nélkül"
    ),
    "boneless": (
        "csont nélkül"
    ),
    "skinless": (
        "bőr nélkül"
    ),
}


UNICODE_FRACTIONS = {
    "½": "1/2",
    "⅓": "1/3",
    "⅔": "2/3",
    "¼": "1/4",
    "¾": "3/4",
    "⅕": "1/5",
    "⅖": "2/5",
    "⅗": "3/5",
    "⅘": "4/5",
    "⅙": "1/6",
    "⅚": "5/6",
    "⅛": "1/8",
    "⅜": "3/8",
    "⅝": "5/8",
    "⅞": "7/8",
}


def normalize_fraction_characters(
    value,
):
    value = str(
        value or ""
    ).strip()

    for source, replacement in (
        UNICODE_FRACTIONS.items()
    ):
        value = value.replace(
            source,
            f" {replacement} ",
        )

    return " ".join(
        value.split()
    )


def fraction_to_decimal(
    value,
):
    numerator, denominator = (
        value.split(
            "/",
            1,
        )
    )

    denominator_value = Decimal(
        denominator
    )

    if denominator_value == 0:
        raise InvalidOperation

    return (
        Decimal(numerator)
        / denominator_value
    )


def format_decimal_quantity(
    value,
):
    if value is None:
        return ""

    value = value.quantize(
        Decimal("0.000001"),
        rounding=ROUND_HALF_UP,
    )

    text = format(
        value,
        "f",
    )

    if "." in text:
        text = (
            text
            .rstrip("0")
            .rstrip(".")
        )

    return text


def parse_quantity_prefix(
    value,
):
    value = (
        normalize_fraction_characters(
            value
        )
    )

    if not value:
        return (
            None,
            "",
        )

    parts = value.split()

    if not parts:
        return (
            None,
            "",
        )

    first = parts[0]

    if re.fullmatch(
        r"\d+\s*[-–]\s*\d+",
        first,
    ):
        return (
            None,
            value,
        )

    quantity = None
    consumed = 0

    try:
        if re.fullmatch(
            r"\d+/\d+",
            first,
        ):
            quantity = (
                fraction_to_decimal(
                    first
                )
            )

            consumed = 1

        elif re.fullmatch(
            r"\d+(?:\.\d+)?",
            first,
        ):
            quantity = Decimal(
                first
            )

            consumed = 1

            if (
                len(parts) > 1
                and re.fullmatch(
                    r"\d+/\d+",
                    parts[1],
                )
            ):
                quantity += (
                    fraction_to_decimal(
                        parts[1]
                    )
                )

                consumed = 2

        else:
            return (
                None,
                value,
            )

    except (
        InvalidOperation,
        ValueError,
        ZeroDivisionError,
    ):
        return (
            None,
            value,
        )

    remainder = " ".join(
        parts[consumed:]
    ).strip()

    return (
        quantity,
        remainder,
    )
    value = (
        normalize_fraction_characters(
            value
        )
    )

    if not value:
        return (
            None,
            "",
        )

    if re.match(
        r"^\d+\s*[-–]\s*\d+",
        value,
    ):
        return (
            None,
            value,
        )

    match = re.match(
        (
            r"^"
            r"(?P<number>\d+(?:\.\d+)?)?"
            r"(?:\s+)?"
            r"(?P<fraction>\d+/\d+)?"
            r"(?:\s+)?"
            r"(?P<rest>.*)"
            r"$"
        ),
        value,
    )

    if match is None:
        return (
            None,
            value,
        )

    number_text = (
        match.group("number")
    )

    fraction_text = (
        match.group("fraction")
    )

    if (
        number_text is None
        and fraction_text is None
    ):
        return (
            None,
            value,
        )

    quantity = Decimal("0")

    try:
        if number_text:
            quantity += Decimal(
                number_text
            )

        if fraction_text:
            quantity += (
                fraction_to_decimal(
                    fraction_text
                )
            )

    except (
        InvalidOperation,
        ValueError,
        ZeroDivisionError,
    ):
        return (
            None,
            value,
        )

    return (
        quantity,
        (
            match.group("rest")
            or ""
        ).strip(),
    )


def get_themealdb_import_ingredient_map():
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

    result = {}
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

        hungarian_name = next(
            (
                translation.name.strip()
                for translation
                in ingredient.translations
                if (
                    translation.language_code
                    == "hu"
                    and translation.name
                    and translation.name.strip()
                )
            ),
            None,
        )

        for english_name in (
            english_names
        ):
            if english_name in result:
                duplicate_names.add(
                    english_name
                )
                continue

            result[english_name] = {
                "ingredient_id": (
                    ingredient.id
                ),
                "hungarian_name": (
                    hungarian_name
                ),
            }

    for duplicate_name in (
        duplicate_names
    ):
        result.pop(
            duplicate_name,
            None,
        )

    return result


def get_active_unit_code_map():
    units = db.session.scalars(
        select(Unit)
        .where(
            Unit.is_active.is_(
                True
            )
        )
    ).all()

    return {
        unit.code: unit
        for unit in units
    }


def normalize_themealdb_measure(
    measure,
    unit_code_map,
):
    raw_measure = str(
        measure or ""
    ).strip()

    if not raw_measure:
        return {
            "quantity": "",
            "unit_id": 0,
            "unit_text": "",
            "note_text": "",
        }

    lowered_measure = (
        raw_measure.casefold()
    )

    direct_text = (
        THEMEALDB_HU_UNIT_TEXT.get(
            lowered_measure
        )
    )

    if direct_text:
        return {
            "quantity": "",
            "unit_id": 0,
            "unit_text": direct_text,
            "note_text": "",
        }

    quantity, remainder = (
        parse_quantity_prefix(
            raw_measure
        )
    )

    if quantity is None:
        return {
            "quantity": "",
            "unit_id": 0,
            "unit_text": (
                THEMEALDB_HU_UNIT_TEXT.get(
                    lowered_measure,
                    raw_measure,
                )
            ),
            "note_text": "",
        }

    remainder = (
        remainder
        .strip()
        .rstrip(".")
    )

    remainder_key = (
        remainder.casefold()
    )

    for (
        unit_alias,
        unit_code,
    ) in sorted(
        THEMEALDB_UNIT_ALIASES.items(),
        key=lambda item: len(
            item[0]
        ),
        reverse=True,
    ):
        if (
            remainder_key
            == unit_alias
        ):
            extra_text = ""

        elif remainder_key.startswith(
            unit_alias + " "
        ):
            extra_text = (
                remainder[
                    len(unit_alias):
                ]
                .strip()
            )

        else:
            continue

        if unit_code not in unit_code_map:
            continue

        unit = unit_code_map[
            unit_code
        ]

        translated_note = (
            THEMEALDB_MEASURE_NOTE_TRANSLATIONS
            .get(
                extra_text.casefold(),
                extra_text,
            )
            if extra_text
            else ""
        )

        return {
            "quantity": format_decimal_quantity(
                quantity
            ),
            "unit_id": unit.id,
            "unit_text": (
                THEMEALDB_UNIT_DISPLAY_TEXT
                .get(
                    unit.code,
                    unit.symbol,
                )
            ),
            "note_text": (
                translated_note
            ),
        }

    translated_unit_text = (
        THEMEALDB_HU_UNIT_TEXT.get(
            remainder_key
        )
    )

    if translated_unit_text:
        return {
            "quantity": format_decimal_quantity(
                quantity
            ),
            "unit_id": 0,
            "unit_text": (
                translated_unit_text
            ),
            "note_text": "",
        }

    return {
        "quantity": format_decimal_quantity(
            quantity
        ),
        "unit_id": 0,
        "unit_text": remainder,
        "note_text": "",
    }


def normalize_themealdb_import_ingredients(
    imported_recipe,
):
    ingredient_map = (
        get_themealdb_import_ingredient_map()
    )

    unit_code_map = (
        get_active_unit_code_map()
    )

    rows = []

    for item in (
        imported_recipe.get(
            "ingredients"
        )
        or []
    ):
        original_name = str(
            item.get("name")
            or ""
        ).strip()

        if not original_name:
            continue

        lookup_name = (
            original_name.casefold()
        )

        normalized_lookup_name = (
            THEMEALDB_IMPORT_INGREDIENT_ALIASES
            .get(
                lookup_name,
                lookup_name,
            )
        )

        matched = (
            ingredient_map.get(
                normalized_lookup_name
            )
        )

        if matched is not None:
            ingredient_id = (
                matched[
                    "ingredient_id"
                ]
            )

            display_name = (
                matched[
                    "hungarian_name"
                ]
                or original_name
            )

        else:
            ingredient_id = 0

            display_name = (
                THEMEALDB_FALLBACK_HU_NAMES
                .get(
                    lookup_name,
                    original_name,
                )
            )

        measure_data = (
            normalize_themealdb_measure(
                item.get("measure"),
                unit_code_map,
            )
        )

        rows.append(
            {
                "ingredient_id": (
                    ingredient_id
                ),
                "name": display_name,
                "quantity": (
                    measure_data[
                        "quantity"
                    ]
                ),
                "unit_id": (
                    measure_data[
                        "unit_id"
                    ]
                ),
                "unit_text": (
                    measure_data[
                        "unit_text"
                    ]
                ),
                "note": (
                    measure_data[
                        "note_text"
                    ]
                ),
                "source_name": (
                    original_name
                ),
                "source_measure": (
                    item.get("measure")
                    or ""
                ),
            }
        )

    return rows
