import json
import urllib.parse
import urllib.request

from flask import current_app

THEMEALDB_CUISINE_MAP = {
    "hungarian": "Hungarian",
    "italian": "Italian",
    "indian": "Indian",
    "mexican": "Mexican",
    "chinese": "Chinese",
    "japanese": "Japanese",
    "american": "American",
}


THEMEALDB_FOOD_TYPE_MAP = {
    "pasta_dish": "Pasta",
    "side_dish": "Side",
    "dessert": "Dessert",
    "breakfast": "Breakfast",
}


THEMEALDB_DIET_MAP = {
    "vegetarian": "Vegetarian",
    "vegan": "Vegan",
}

def themealdb_request(
    endpoint,
    params=None,
):
    api_key = str(
        current_app.config[
            "THEMEALDB_API_KEY"
        ]
    )

    base_url = (
        current_app.config[
            "THEMEALDB_API_BASE_URL"
        ]
        .rstrip("/")
    )

    query_string = (
        urllib.parse.urlencode(
            params or {}
        )
    )

    url = (
        f"{base_url}/"
        f"{api_key}/"
        f"{endpoint}"
    )

    if query_string:
        url = (
            f"{url}?"
            f"{query_string}"
        )

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "HomePantry/1.0"
            ),
            "Accept": (
                "application/json"
            ),
        },
    )

    timeout = int(
        current_app.config.get(
            "ONLINE_RECIPE_TIMEOUT",
            15,
        )
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=timeout,
        ) as response:
            return json.load(
                response
            )

    except (
        urllib.error.HTTPError,
        urllib.error.URLError,
        TimeoutError,
        json.JSONDecodeError,
    ) as exc:
        raise RuntimeError(
            "Online recipe service "
            "is unavailable."
        ) from exc


def extract_themealdb_ingredients(
    meal,
):
    ingredients = []

    for index in range(
        1,
        21,
    ):
        name = (
            meal.get(
                f"strIngredient{index}"
            )
            or ""
        ).strip()

        measure = (
            meal.get(
                f"strMeasure{index}"
            )
            or ""
        ).strip()

        if not name:
            continue

        ingredients.append(
            {
                "name": name,
                "measure": measure,
            }
        )

    return ingredients


def normalize_themealdb_meal(
    meal,
):
    return {
        "provider": "themealdb",
        "external_id": (
            str(
                meal.get("idMeal")
                or ""
            )
        ),
        "title": (
            meal.get("strMeal")
            or ""
        ),
        "category": (
            meal.get("strCategory")
            or ""
        ),
        "area": (
            meal.get("strArea")
            or ""
        ),
        "instructions": (
            meal.get(
                "strInstructions"
            )
            or ""
        ),
        "image_url": (
            meal.get(
                "strMealThumb"
            )
            or ""
        ),
        "source_url": (
            meal.get("strSource")
            or ""
        ),
        "youtube_url": (
            meal.get("strYoutube")
            or ""
        ),
        "ingredients": (
            extract_themealdb_ingredients(
                meal
            )
        ),
    }


def search_themealdb_recipes(
    query,
    area=None,
    category=None,
):
    query = (
        str(query or "")
        .strip()
    )

    if len(query) < 2:
        return []

    data = themealdb_request(
        "search.php",
        {
            "s": query,
        },
    )

    meals = (
        data.get("meals")
        or []
    )

    results = []

    for meal in meals:
        if (
            area
            and meal.get("strArea")
            != area
        ):
            continue

        if (
            category
            and meal.get("strCategory")
            != category
        ):
            continue

        results.append(
            normalize_themealdb_meal(
                meal
            )
        )

    return results
    query = (
        str(query or "")
        .strip()
    )

    if len(query) < 2:
        return []

    data = themealdb_request(
        "search.php",
        {
            "s": query,
        },
    )

    meals = (
        data.get("meals")
        or []
    )

    return [
        normalize_themealdb_meal(
            meal
        )
        for meal in meals
    ]


def get_themealdb_recipe(
    external_id,
):
    external_id = (
        str(external_id or "")
        .strip()
    )

    if not external_id:
        return None

    data = themealdb_request(
        "lookup.php",
        {
            "i": external_id,
        },
    )

    meals = (
        data.get("meals")
        or []
    )

    if not meals:
        return None

    return normalize_themealdb_meal(
        meals[0]
    )
