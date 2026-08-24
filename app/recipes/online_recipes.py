import html
import json
import re
import urllib.error
import urllib.parse
import urllib.request

from flask import current_app

THEMEALDB_IMAGE_HOSTS = {
    "themealdb.com",
    "www.themealdb.com",
}


def download_themealdb_image(
    image_url,
):
    image_url = (
        str(image_url or "")
        .strip()
    )

    if not image_url:
        raise RuntimeError(
            "Missing image URL."
        )

    parsed_url = (
        urllib.parse.urlparse(
            image_url
        )
    )

    if (
        parsed_url.scheme != "https"
        or parsed_url.hostname
        not in THEMEALDB_IMAGE_HOSTS
    ):
        raise RuntimeError(
            "Invalid TheMealDB image URL."
        )

    request = urllib.request.Request(
        image_url,
        headers={
            "User-Agent": (
                "HomePantry/1.0"
            ),
            "Accept": "image/*",
        },
    )

    timeout = int(
        current_app.config.get(
            "ONLINE_RECIPE_TIMEOUT",
            15,
        )
    )

    max_bytes = int(
        current_app.config.get(
            "ONLINE_RECIPE_IMAGE_MAX_BYTES",
            10 * 1024 * 1024,
        )
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=timeout,
        ) as response:
            final_url = (
                response.geturl()
            )

            final_parsed = (
                urllib.parse.urlparse(
                    final_url
                )
            )

            if (
                final_parsed.scheme
                != "https"
                or final_parsed.hostname
                not in THEMEALDB_IMAGE_HOSTS
            ):
                raise RuntimeError(
                    "Invalid redirected "
                    "image URL."
                )

            content_type = (
                response.headers.get(
                    "Content-Type",
                    "",
                )
                .split(
                    ";",
                    1,
                )[0]
                .strip()
                .lower()
            )

            if not content_type.startswith(
                "image/"
            ):
                raise RuntimeError(
                    "Remote file is not "
                    "an image."
                )

            content_length = (
                response.headers.get(
                    "Content-Length"
                )
            )

            if content_length:
                try:
                    if (
                        int(content_length)
                        > max_bytes
                    ):
                        raise RuntimeError(
                            "Remote image "
                            "is too large."
                        )
                except ValueError:
                    pass

            data = response.read(
                max_bytes + 1
            )

    except (
        urllib.error.HTTPError,
        urllib.error.URLError,
        TimeoutError,
    ) as exc:
        raise RuntimeError(
            "Unable to download "
            "TheMealDB image."
        ) from exc

    if (
        not data
        or len(data) > max_bytes
    ):
        raise RuntimeError(
            "Invalid or oversized "
            "remote image."
        )

    return data

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


def clean_themealdb_instructions(
    value,
):
    value = str(
        value or ""
    )

    value = re.sub(
        r"(?i)<br\s*/?>",
        "\n",
        value,
    )

    value = re.sub(
        r"(?i)</p\s*>",
        "\n\n",
        value,
    )

    value = re.sub(
        r"(?i)<p(?:\s[^>]*)?>",
        "",
        value,
    )

    value = re.sub(
        r"<[^>]+>",
        "",
        value,
    )

    value = html.unescape(
        value
    )

    lines = [
        line.strip()
        for line in value.splitlines()
    ]

    cleaned_lines = []
    previous_blank = False

    for line in lines:
        is_blank = not line

        if (
            is_blank
            and previous_blank
        ):
            continue

        cleaned_lines.append(
            line
        )

        previous_blank = (
            is_blank
        )

    return "\n".join(
        cleaned_lines
    ).strip()


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
            clean_themealdb_instructions(
                meal.get(
                    "strInstructions"
                )
            )
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
