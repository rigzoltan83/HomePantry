import re

import requests
from flask import current_app


OFF_PRODUCT_URL = (
    "https://world.openfoodfacts.org"
    "/api/v2/product/{barcode}.json"
)


def _parse_quantity(
    quantity_text,
):
    if not quantity_text:
        return (
            None,
            None,
        )

    normalized = (
        str(quantity_text)
        .strip()
        .lower()
        .replace(",", ".")
    )

    match = re.search(
        r"(\d+(?:\.\d+)?)\s*"
        r"(kg|g|mg|l|ml|cl)\b",
        normalized,
    )

    if match is None:
        return (
            None,
            None,
        )

    try:
        quantity = float(
            match.group(1)
        )
    except ValueError:
        return (
            None,
            None,
        )

    return (
        quantity,
        match.group(2),
    )


def lookup_open_food_facts(
    barcode,
):
    barcode = str(
        barcode
    ).strip()

    if not barcode:
        return None

    try:
        response = requests.get(
            OFF_PRODUCT_URL.format(
                barcode=barcode
            ),
            params={
                "fields": (
                    "code,"
                    "product_name,"
                    "product_name_hu,"
                    "product_name_en,"
                    "generic_name,"
                    "generic_name_hu,"
                    "generic_name_en,"
                    "brands,"
                    "quantity,"
                    "ingredients_text,"
                    "ingredients_text_hu,"
                    "ingredients_text_en,"
                    "ingredients,"
                    "ingredients_tags,"
                    "allergens,"
                    "allergens_tags,"
                    "traces,"
                    "traces_tags,"
                    "categories,"
                    "categories_tags,"
                    "labels,"
                    "labels_tags,"
                    "nutriments,"
                    "nova_group"
                ),
                "lc": "hu",
                "tags_lc": "hu",
            },
            headers={
                "User-Agent": (
                    current_app.config[
                        "OPEN_FOOD_FACTS_USER_AGENT"
                    ]
                ),
                "Accept": (
                    "application/json"
                ),
            },
            timeout=(
                2.0,
                4.0,
            ),
        )

        if response.status_code == 404:
            return None

        response.raise_for_status()

        data = response.json()

    except (
        requests.RequestException,
        ValueError,
    ):
        current_app.logger.exception(
            "Open Food Facts lookup failed "
            "for barcode %s",
            barcode,
        )

        return None

    if (
        data.get("status") != 1
        or not data.get("product")
    ):
        return None

    product = data["product"]

    name = (
        product.get(
            "product_name_hu"
        )
        or product.get(
            "product_name"
        )
        or ""
    ).strip()

    brands = (
        product.get("brands")
        or ""
    ).strip()

    quantity_text = (
        product.get("quantity")
        or ""
    ).strip()

    (
        package_quantity,
        package_unit_symbol,
    ) = _parse_quantity(
        quantity_text
    )

    name_hu = (
        product.get(
            "product_name_hu"
        )
        or ""
    ).strip()

    name_en = (
        product.get(
            "product_name_en"
        )
        or ""
    ).strip()

    fallback_name = (
        product.get(
            "product_name"
        )
        or ""
    ).strip()

    name = (
        name_hu
        or name_en
        or fallback_name
    )

    generic_name_hu = (
        product.get(
            "generic_name_hu"
        )
        or ""
    ).strip()

    generic_name_en = (
        product.get(
            "generic_name_en"
        )
        or ""
    ).strip()

    ingredients_text_hu = (
        product.get(
            "ingredients_text_hu"
        )
        or ""
    ).strip()

    ingredients_text_en = (
        product.get(
            "ingredients_text_en"
        )
        or ""
    ).strip()

    fallback_ingredients_text = (
        product.get(
            "ingredients_text"
        )
        or ""
    ).strip()

    if (
        not ingredients_text_hu
        and fallback_ingredients_text
    ):
        ingredients_text_hu = (
            fallback_ingredients_text
        )

    if (
        not ingredients_text_en
        and fallback_ingredients_text
    ):
        ingredients_text_en = (
            fallback_ingredients_text
        )

    external_data = {
        "ingredients": (
            product.get(
                "ingredients"
            )
            or []
        ),
        "ingredients_tags": (
            product.get(
                "ingredients_tags"
            )
            or []
        ),
        "allergens": (
            product.get(
                "allergens"
            )
            or ""
        ),
        "allergens_tags": (
            product.get(
                "allergens_tags"
            )
            or []
        ),
        "traces": (
            product.get(
                "traces"
            )
            or ""
        ),
        "traces_tags": (
            product.get(
                "traces_tags"
            )
            or []
        ),
        "categories": (
            product.get(
                "categories"
            )
            or ""
        ),
        "categories_tags": (
            product.get(
                "categories_tags"
            )
            or []
        ),
        "labels": (
            product.get(
                "labels"
            )
            or ""
        ),
        "labels_tags": (
            product.get(
                "labels_tags"
            )
            or []
        ),
        "nutriments": (
            product.get(
                "nutriments"
            )
            or {}
        ),
        "nova_group": (
            product.get(
                "nova_group"
            )
        ),
    }

    return {
        "barcode": barcode,

        "name": name,
        "name_hu": (
            name_hu
            or None
        ),
        "name_en": (
            name_en
            or None
        ),

        "generic_name_hu": (
            generic_name_hu
            or None
        ),
        "generic_name_en": (
            generic_name_en
            or None
        ),

        "brand": brands,

        "quantity_text": (
            quantity_text
        ),
        "package_quantity": (
            package_quantity
        ),
        "package_unit_symbol": (
            package_unit_symbol
        ),

        "ingredients_text_hu": (
            ingredients_text_hu
            or None
        ),
        "ingredients_text_en": (
            ingredients_text_en
            or None
        ),

        "external_data": (
            external_data
        ),
    }
