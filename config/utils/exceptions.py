from rest_framework.views import exception_handler as drf_exception_handler

from config.utils.translation import request_language, translate

ERROR_TRANSLATIONS = {
    "required": "errors.required",
    "blank": "errors.blank",
    "invalid": "errors.invalid",
    "unique": "errors.unique",
    "does_not_exist": "errors.not_found",
    "not_found": "errors.not_found",
    "not_authenticated": "errors.not_authenticated",
    "authentication_failed": "errors.authentication_failed",
    "permission_denied": "errors.permission_denied",
    "method_not_allowed": "errors.method_not_allowed",
    "parse_error": "errors.parse_error",
    "throttled": "errors.throttled",
    "max_length": "errors.max_length",
    "min_length": "errors.min_length",
    "max_value": "errors.max_value",
    "min_value": "errors.min_value",
}


def _translate_details(details, language):
    if isinstance(details, dict):
        return {
            key: (
                str(value) if key == "message" else _translate_details(value, language)
            )
            for key, value in details.items()
        }

    if isinstance(details, (list, tuple)):
        return [_translate_details(item, language) for item in details]

    code = getattr(details, "code", None)

    if code:
        key = ERROR_TRANSLATIONS.get(code, code)
        
        try:
            return translate(key, language=language)
        except (KeyError, ValueError):
            pass

    return str(details)


def translated_exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    if response is None:
        return None

    request = context.get("request")
    language = request_language(request)
    details = _translate_details(response.data, language)

    if isinstance(details, dict) and ("message" in details or "detail" in details):
        message = details.get("message", details.get("detail"))
        errors = {
            key: value
            for key, value in details.items()
            if key not in {"message", "detail"}
        }
        response.data = {"message": message}
        if errors:
            response.data["errors"] = errors
    else:
        try:
            message = translate("errors.request_failed", language=language)
        except (KeyError, ValueError):
            message = "Request failed."
        response.data = {"message": message, "errors": details}

    return response
