from datetime import (
    date,
    timedelta,
)
from decimal import Decimal

from flask import render_template
from flask_login import (
    current_user,
    login_required,
)
from sqlalchemy import select

from app.extensions import db
from app.models import (
    HouseholdMember,
    InventoryBatch,
    InventoryMovement,
    StockRule,
)

from . import bp


DASHBOARD_MOVEMENT_LIMIT = 8


def get_ingredient_name(
    ingredient,
):
    language_code = (
        current_user.preferred_language
        or "hu"
    )

    name = next(
        (
            translation.name
            for translation
            in ingredient.translations
            if translation.language_code
            == language_code
        ),
        None,
    )

    if name is None:
        name = next(
            (
                translation.name
                for translation
                in ingredient.translations
                if translation.language_code
                == "hu"
            ),
            None,
        )

    return (
        name
        or ingredient.canonical_key
    )


def format_quantity(
    value,
):
    value = Decimal(value)

    normalized = format(
        value.normalize(),
        "f",
    )

    if "." in normalized:
        normalized = (
            normalized
            .rstrip("0")
            .rstrip(".")
        )

    return normalized


@bp.get("/")
@login_required
def index():
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

    household = (
        membership.household
        if membership is not None
        else None
    )

    if household is None:
        return render_template(
            "main/index.html",
            household=None,
            membership=None,
            inventory_batch_count=0,
            inventory_ingredient_count=0,
            expired_count=0,
            expiring_count=0,
            low_stock_count=0,
            low_stock_items=[],
            expiring_items=[],
            recent_movements=[],
        )

    household_id = household.id

    today = date.today()

    expiring_limit = (
        today
        + timedelta(
            days=household.expiring_soon_days
        )
    )

    batches = db.session.scalars(
        select(InventoryBatch)
        .where(
            InventoryBatch.household_id
            == household_id,
            InventoryBatch.is_active.is_(
                True
            ),
            InventoryBatch.quantity > 0,
        )
        .order_by(
            InventoryBatch.expiration_date
            .asc()
            .nullslast(),
            InventoryBatch.created_at,
        )
    ).all()

    inventory_batch_count = len(
        batches
    )

    inventory_ingredient_count = len(
        {
            batch.ingredient_id
            for batch in batches
        }
    )

    expired_batches = [
        batch
        for batch in batches
        if (
            batch.expiration_date
            and batch.expiration_date
            < today
        )
    ]

    expiring_batches = [
        batch
        for batch in batches
        if (
            batch.expiration_date
            and today
            <= batch.expiration_date
            <= expiring_limit
        )
    ]

    expired_count = len(
        expired_batches
    )

    expiring_count = len(
        expiring_batches
    )

    expiring_items = []

    for batch in (
        expired_batches
        + expiring_batches
    )[:6]:
        expiring_items.append(
            {
                "ingredient_name": (
                    get_ingredient_name(
                        batch.ingredient
                    )
                ),
                "product_name": (
                    batch.product.name
                    if batch.product
                    else None
                ),
                "quantity": (
                    format_quantity(
                        batch.quantity
                    )
                ),
                "unit": batch.unit.symbol,
                "expiration_date": (
                    batch.expiration_date
                ),
                "is_expired": (
                    batch.expiration_date
                    < today
                ),
            }
        )

    rules = db.session.scalars(
        select(StockRule)
        .where(
            StockRule.household_id
            == household_id,
            StockRule.is_active.is_(
                True
            ),
        )
        .order_by(
            StockRule.id
        )
    ).all()

    low_stock_items = []

    for rule in rules:
        current_base_quantity = Decimal(
            "0"
        )

        for batch in batches:
            if (
                batch.ingredient_id
                != rule.ingredient_id
            ):
                continue

            if (
                batch.unit.dimension
                != rule.unit.dimension
            ):
                continue

            current_base_quantity += (
                Decimal(
                    batch.quantity
                )
                * Decimal(
                    batch.unit.factor_to_base
                )
            )

        minimum_base_quantity = (
            Decimal(
                rule.minimum_quantity
            )
            * Decimal(
                rule.unit.factor_to_base
            )
        )

        if (
            current_base_quantity
            >= minimum_base_quantity
        ):
            continue

        current_quantity = (
            current_base_quantity
            / Decimal(
                rule.unit.factor_to_base
            )
        )

        low_stock_items.append(
            {
                "ingredient_name": (
                    get_ingredient_name(
                        rule.ingredient
                    )
                ),
                "current_quantity": (
                    format_quantity(
                        current_quantity
                    )
                ),
                "minimum_quantity": (
                    format_quantity(
                        rule.minimum_quantity
                    )
                ),
                "unit": (
                    rule.unit.symbol
                ),
            }
        )

    low_stock_items.sort(
        key=lambda item: (
            item[
                "ingredient_name"
            ].lower()
        )
    )

    low_stock_count = len(
        low_stock_items
    )

    recent_movements = (
        db.session.scalars(
            select(InventoryMovement)
            .where(
                InventoryMovement.household_id
                == household_id
            )
            .order_by(
                InventoryMovement.created_at
                .desc(),
                InventoryMovement.id.desc(),
            )
            .limit(
                DASHBOARD_MOVEMENT_LIMIT
            )
        )
        .all()
    )

    return render_template(
        "main/index.html",
        household=household,
        membership=membership,
        inventory_batch_count=(
            inventory_batch_count
        ),
        inventory_ingredient_count=(
            inventory_ingredient_count
        ),
        expired_count=expired_count,
        expiring_count=expiring_count,
        low_stock_count=(
            low_stock_count
        ),
        low_stock_items=(
            low_stock_items[:6]
        ),
        expiring_items=(
            expiring_items
        ),
        recent_movements=(
            recent_movements
        ),
        get_ingredient_name=(
            get_ingredient_name
        ),
        format_quantity=(
            format_quantity
        ),
    )
