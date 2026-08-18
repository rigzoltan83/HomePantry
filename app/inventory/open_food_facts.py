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
                    "brands,"
                    "quantity,"
                    "image_front_url,"
                    "image_front_small_url"
                ),
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

    return {
        "barcode": barcode,
        "name": name,
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
        "image_url": (
            product.get(
                "image_front_url"
            )
            or product.get(
                "image_front_small_url"
            )
            or None
        ),
    }
