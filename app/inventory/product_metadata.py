from copy import deepcopy
from .open_food_facts import (
    OpenFoodFactsTemporaryUnavailable,
    lookup_open_food_facts,
)


def is_missing_value(
    value,
):
    if value is None:
        return True

    if isinstance(
        value,
        str,
    ):
        return not value.strip()

    if isinstance(
        value,
        (
            list,
            dict,
        ),
    ):
        return len(value) == 0

    return False


def merge_external_data(
    existing,
    incoming,
):
    """
    Non-destructive merge.

    - Existing scalar values are never replaced.
    - Missing scalar values may be filled.
    - Dictionaries are merged recursively.
    - Lists keep all existing items and gain
      new unique items from the incoming list.
    """

    if is_missing_value(existing):
        return deepcopy(
            incoming
        )

    if is_missing_value(incoming):
        return deepcopy(
            existing
        )

    if (
        isinstance(existing, dict)
        and isinstance(incoming, dict)
    ):
        result = deepcopy(
            existing
        )

        for key, incoming_value in (
            incoming.items()
        ):
            if key not in result:
                result[key] = deepcopy(
                    incoming_value
                )

                continue

            result[key] = (
                merge_external_data(
                    result[key],
                    incoming_value,
                )
            )

        return result

    if (
        isinstance(existing, list)
        and isinstance(incoming, list)
    ):
        result = deepcopy(
            existing
        )

        for incoming_item in incoming:
            if incoming_item not in result:
                result.append(
                    deepcopy(
                        incoming_item
                    )
                )

        return result

    return deepcopy(
        existing
    )

def fill_missing_product_metadata(
    product,
    external_product,
):
    changes = 0

    scalar_fields = (
        (
            "name_hu",
            external_product.get(
                "name_hu"
            ),
        ),
        (
            "name_en",
            external_product.get(
                "name_en"
            ),
        ),
        (
            "generic_name_hu",
            external_product.get(
                "generic_name_hu"
            ),
        ),
        (
            "generic_name_en",
            external_product.get(
                "generic_name_en"
            ),
        ),
        (
            "ingredients_text_hu",
            external_product.get(
                "ingredients_text_hu"
            ),
        ),
        (
            "ingredients_text_en",
            external_product.get(
                "ingredients_text_en"
            ),
        ),
        (
            "external_source",
            "open_food_facts",
        ),
        (
            "external_source_id",
            external_product.get(
                "barcode"
            ),
        ),
    )

    for field_name, incoming_value in (
        scalar_fields
    ):
        current_value = getattr(
            product,
            field_name,
        )

        if (
            is_missing_value(
                current_value
            )
            and not is_missing_value(
                incoming_value
            )
        ):
            setattr(
                product,
                field_name,
                incoming_value,
            )

            changes += 1

    existing_external_data = (
        product.external_data
        or {}
    )

    incoming_external_data = (
        external_product.get(
            "external_data"
        )
        or {}
    )

    merged_external_data = (
        merge_external_data(
            existing_external_data,
            incoming_external_data,
        )
    )

    if (
        merged_external_data
        != existing_external_data
    ):
        product.external_data = (
            merged_external_data
        )

        changes += 1

    return changes

def refresh_product_metadata(
    product,
):
    barcode = None

    for barcode_record in (
        product.barcodes
        or []
    ):
        value = (
            barcode_record.barcode
            or ""
        ).strip()

        if value:
            barcode = value
            break

    if not barcode:
        return {
            "found": False,
            "changed": False,
            "changes": 0,
            "barcode": None,
            "reason": "no_barcode",
            "status_code": None,
            "retry_after": None,
        }

    try:
        external_product = (
            lookup_open_food_facts(
                barcode
            )
        )

    except OpenFoodFactsTemporaryUnavailable as exc:
        return {
            "found": False,
            "changed": False,
            "changes": 0,
            "barcode": barcode,
            "reason": (
                "rate_limited"
                if exc.status_code == 429
                else "temporary_unavailable"
            ),
            "status_code": (
                exc.status_code
            ),
            "retry_after": (
                exc.retry_after
            ),
        }

    if external_product is None:
        return {
            "found": False,
            "changed": False,
            "changes": 0,
            "barcode": barcode,
            "reason": "not_found",
            "status_code": None,
            "retry_after": None,
        }

    changes = (
        fill_missing_product_metadata(
            product,
            external_product,
        )
    )

    return {
        "found": True,
        "changed": (
            changes > 0
        ),
        "changes": changes,
        "barcode": barcode,
        "reason": None,
        "status_code": None,
        "retry_after": None,
    }
