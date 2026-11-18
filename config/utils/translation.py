import json
from functools import lru_cache
from pathlib import Path

from django.conf import settings

LOCALES_DIR = Path(__file__).resolve().parents[1] / "locales"


@lru_cache(maxsize=None)
def load_translations(language):
    file_path = LOCALES_DIR / f"{language}.json"

    try:
        with file_path.open("r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        raise ValueError(f"Unsupported language: {language}")


def translate(key, language=None, **kwargs):
    language = language or settings.DEFAULT_LANGUAGE
    translations = load_translations(language)

    value = translations

    for part in key.split("."):
        if not isinstance(value, dict) or part not in value:
            raise KeyError(f"Translation key not found: {key}")

        value = value[part]

    if not isinstance(value, str):
        raise ValueError(f"Invalid translation value: {key}")

    return value.format(**kwargs)


def request_language(request):
    supported = set(settings.SUPPORTED_LANGUAGES)
    requested = request.query_params.get("language") if request else None
    if not requested and request:
        requested = request.headers.get("Accept-Language", "").split(",", 1)[0].split("-", 1)[0]
    return requested if requested in supported else None
