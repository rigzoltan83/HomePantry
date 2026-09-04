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

from scripts.seed_units import seed_units
from scripts.seed_ingredient_categories import (
    seed_categories,
)
from scripts.seed_ingredients import (
    seed_ingredients,
)
from scripts.seed_ingredient_units import (
    seed_ingredient_units,
)
from scripts.seed_ingredient_substitutions import (
    seed_substitutions,
)


def seed_reference_data():
    seed_units()
    print("Units: OK")

    seed_categories()
    print("Ingredient categories: OK")

    seed_ingredients()
    print("Ingredients: OK")

    seed_ingredient_units()
    print("Ingredient unit mappings: OK")

    seed_substitutions()
    print("Ingredient substitutions: OK")


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        seed_reference_data()

    print(
        "HomePantry reference data "
        "seeded successfully."
    )
