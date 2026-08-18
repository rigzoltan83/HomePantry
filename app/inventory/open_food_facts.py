import re

import requests
from flask import current_app


OFF_PRODUCT_URL = (
    "https://world.openfoodfacts.org"
    "/api/v2/product/{barcode}.json"
)

OFF_TAXONOMY_DISPLAY_URL = (
    "https://world.openfoodfacts.org"
    "/api/v3/taxonomy_display_tags"
)

TAXONOMY_DISPLAY_CACHE = {}

class OpenFoodFactsTemporaryUnavailable(
    Exception
):
    def __init__(
        self,
        status_code,
        retry_after=None,
    ):
        self.status_code = (
            status_code
        )

        self.retry_after = (
            retry_after
        )

        super().__init__(
            (
                "Open Food Facts temporarily "
                f"unavailable: HTTP {status_code}"
            )
        )


def get_retry_after_seconds(
    response,
):
    value = response.headers.get(
        "Retry-After"
    )

    if not value:
        return None

    try:
        seconds = int(
            value
        )
    except (
        TypeError,
        ValueError,
    ):
        return None

    return max(
        0,
        seconds,
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


def get_taxonomy_display_tags(
    tagtype,
    canonical_tags,
):
    if (
        not canonical_tags
        or not isinstance(
            canonical_tags,
            list,
        )
    ):
        return {
            "hu": [],
            "en": [],
        }

    canonical_tags = [
        str(tag).strip()
        for tag in canonical_tags
        if str(tag).strip()
    ]

    if not canonical_tags:
        return {
            "hu": [],
            "en": [],
        }

    result = {
        "hu": [],
        "en": [],
    }

    tags_list = ",".join(
        canonical_tags
    )

    cache_key = (
        str(tagtype),
        tuple(
            sorted(
                canonical_tags
            )
        ),
    )

    cached = (
        TAXONOMY_DISPLAY_CACHE.get(
            cache_key
        )
    )

    if cached is not None:
        return {
            "hu": list(
                cached.get(
                    "hu",
                    []
                )
            ),
            "en": list(
                cached.get(
                    "en",
                    []
                )
            ),
        }

    for language in (
        "hu",
        "en",
    ):
        try:
            response = requests.get(
                OFF_TAXONOMY_DISPLAY_URL,
                params={
                    "tagtype": tagtype,
                    "canonical_tags_list": (
                        tags_list
                    ),
                    "lc": language,
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

            if response.status_code in {
                429,
                503,
            }:
                raise (
                    OpenFoodFactsTemporaryUnavailable(
                        response.status_code,
                        get_retry_after_seconds(
                            response
                        ),
                    )
                )

            response.raise_for_status()

            data = response.json()

        except (
            OpenFoodFactsTemporaryUnavailable
        ):
            raise

        except (
            requests.RequestException,
            ValueError,
        ):
            current_app.logger.exception(
                (
                    "Open Food Facts taxonomy "
                    "lookup failed for %s / %s"
                ),
                tagtype,
                language,
            )

            continue

        if (
            data.get("status")
            != "success"
        ):
            continue

        local_tags_list = (
            data.get(
                "local_tags_list"
            )
            or ""
        )

        result[language] = [
            value.strip()
            for value in (
                local_tags_list
                .split(",")
            )
            if value.strip()
        ]

    TAXONOMY_DISPLAY_CACHE[
        cache_key
    ] = {
        "hu": list(
            result["hu"]
        ),
        "en": list(
            result["en"]
        ),
    }

    return result


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

        if response.status_code in {
            429,
            503,
        }:
            raise (
                OpenFoodFactsTemporaryUnavailable(
                    response.status_code,
                    get_retry_after_seconds(
                        response
                    ),
                )
            )

        response.raise_for_status()

        data = response.json()

    except (
        OpenFoodFactsTemporaryUnavailable
    ):
        raise

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

    allergens_tags = (
        product.get(
            "allergens_tags"
        )
        or []
    )

    traces_tags = (
        product.get(
            "traces_tags"
        )
        or []
    )

    categories_tags = (
        product.get(
            "categories_tags"
        )
        or []
    )

    labels_tags = (
        product.get(
            "labels_tags"
        )
        or []
    )

    allergens_display = (
        get_taxonomy_display_tags(
            "allergens",
            allergens_tags,
        )
    )

    traces_display = (
        get_taxonomy_display_tags(
            "allergens",
            traces_tags,
        )
    )

    categories_display = (
        get_taxonomy_display_tags(
            "categories",
            categories_tags,
        )
    )

    labels_display = (
        get_taxonomy_display_tags(
            "labels",
            labels_tags,
        )
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
            allergens_tags
        ),
        "allergens_display": (
            allergens_display
        ),
        "traces": (
            product.get(
                "traces"
            )
            or ""
        ),
        "traces_tags": (
            traces_tags
        ),
        "traces_display": (
            traces_display
        ),
        "categories": (
            product.get(
                "categories"
            )
            or ""
        ),
        "categories_tags": (
            categories_tags
        ),
        "categories_display": (
            categories_display
        ),
        "labels": (
            product.get(
                "labels"
            )
            or ""
        ),
        "labels_tags": (
            labels_tags
        ),
        "labels_display": (
            labels_display
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
