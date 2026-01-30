"""
Custom exception handler for consistent JSON error responses.
Ensures: JSON only, clear field-level errors, no stack traces, uniform structure.
"""
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError


def _normalize_error_detail(detail):
    """
    Convert DRF error detail (dict, list, or string) into a flat dict of
    field -> list of strings for consistent "errors" shape.
    """
    if detail is None:
        return {}
    if isinstance(detail, dict):
        result = {}
        for key, value in detail.items():
            if isinstance(value, list):
                result[key] = [str(item) for item in value]
            else:
                result[key] = [str(value)]
        return result
    if isinstance(detail, list):
        return {"non_field_errors": [str(item) for item in detail]}
    return {"non_field_errors": [str(detail)]}


def custom_exception_handler(exc, context):
    """
    Return consistent JSON error responses: {"message": str, "errors": dict}.
    No stack traces or internal details are exposed.
    """
    response = drf_exception_handler(exc, context)

    if response is not None:
        # Normalize DRF response to consistent structure
        detail = response.data.get("detail", response.data)
        errors = _normalize_error_detail(detail)

        if isinstance(exc, ValidationError):
            message = "Validation failed."
        else:
            # Single message for non-validation (404, 403, etc.)
            if errors:
                first_key = next(iter(errors))
                message = errors[first_key][0] if errors[first_key] else str(exc)
            else:
                message = str(exc) if str(exc) else "Request failed."

        response.data = {"message": message, "errors": errors}
        return response

    # Unhandled exception: return generic 500, never expose stack trace
    return Response(
        {"message": "An unexpected error occurred.", "errors": {}},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
