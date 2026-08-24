import json
import urllib.error
import urllib.request

from flask import current_app


def _clean_translation_text(
    value,
):
    return str(
        value or ""
    ).strip()


def _translate_libre_text(
    text,
    source_language="en",
    target_language="hu",
):
    cleaned_text = (
        _clean_translation_text(
            text
        )
    )

    if not cleaned_text:
        return ""

    max_chars = int(
        current_app.config.get(
            "RECIPE_TRANSLATION_MAX_CHARS",
            15000,
        )
    )

    if len(cleaned_text) > max_chars:
        current_app.logger.warning(
            "Recipe translation skipped: "
            "text too long (%s chars).",
            len(cleaned_text),
        )

        return None

    base_url = (
        current_app.config[
            "RECIPE_TRANSLATION_API_URL"
        ]
    )

    url = (
        f"{base_url}/translate"
    )

    body = json.dumps(
        {
            "q": cleaned_text,
            "source": source_language,
            "target": target_language,
            "format": "text",
        }
    ).encode(
        "utf-8"
    )

    request = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": (
                "application/json"
            ),
            "Accept": (
                "application/json"
            ),
        },
        method="POST",
    )

    timeout = int(
        current_app.config.get(
            "RECIPE_TRANSLATION_TIMEOUT",
            30,
        )
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=timeout,
        ) as response:
            raw_data = (
                response.read()
            )

    except (
        urllib.error.HTTPError,
        urllib.error.URLError,
        TimeoutError,
        OSError,
    ) as exc:
        current_app.logger.warning(
            "LibreTranslate recipe "
            "translation failed: %s",
            exc,
        )

        return None

    try:
        data = json.loads(
            raw_data.decode(
                "utf-8"
            )
        )

    except (
        UnicodeDecodeError,
        json.JSONDecodeError,
    ) as exc:
        current_app.logger.warning(
            "Invalid LibreTranslate "
            "response: %s",
            exc,
        )

        return None

    translated_text = (
        _clean_translation_text(
            data.get(
                "translatedText"
            )
        )
    )

    if not translated_text:
        return None

    return translated_text


def translate_imported_recipe_to_hungarian(
    imported_recipe,
):
    original_title = (
        _clean_translation_text(
            imported_recipe.get(
                "title"
            )
        )
    )

    original_instructions = (
        _clean_translation_text(
            imported_recipe.get(
                "instructions"
            )
        )
    )

    translated_title = (
        _translate_libre_text(
            original_title,
            source_language="en",
            target_language="hu",
        )
    )

    instruction_blocks = [
        block.strip()
        for block in (
            original_instructions
            .split("\n\n")
        )
        if block.strip()
    ]

    translated_blocks = []

    instruction_translation_ok = True

    for block in instruction_blocks:
        translated_block = (
            _translate_libre_text(
                block,
                source_language="en",
                target_language="hu",
            )
        )

        if translated_block is None:
            instruction_translation_ok = False

            translated_blocks.append(
                block
            )

            continue

        translated_blocks.append(
            translated_block
        )

    translated_instructions = (
        "\n\n".join(
            translated_blocks
        )
        if translated_blocks
        else original_instructions
    )

    translated = (
        translated_title is not None
        and instruction_translation_ok
    )

    final_instructions = (
        translated_instructions
        or original_instructions
    )

    if (
        translated_instructions
        and original_instructions
        and translated_instructions.strip()
        != original_instructions.strip()
    ):
        final_instructions = (
            translated_instructions
            + "\n\n"
            + "--- EREDETI ANGOL ---"
            + "\n\n"
            + original_instructions
        )

    return {
        "title": (
            translated_title
            or original_title
        ),
        "instructions": (
            final_instructions
        ),
        "translated": translated,
    }
