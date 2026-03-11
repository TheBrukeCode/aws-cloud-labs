"""
Shared utility functions for the Task API Lambda handlers.
"""
import json
import logging
import os

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────
# HTTP Response Helpers
# ─────────────────────────────────────────

def success(body: dict, status_code: int = 200) -> dict:
    """Return a formatted API Gateway success response."""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(body),
    }


def error(message: str, status_code: int = 400) -> dict:
    """Return a formatted API Gateway error response."""
    logger.error("Returning error %s: %s", status_code, message)
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps({"error": message}),
    }


# ─────────────────────────────────────────
# Request Parsing Helpers
# ─────────────────────────────────────────

def parse_body(event: dict) -> dict:
    """Safely parse the JSON request body from an API Gateway event."""
    try:
        return json.loads(event.get("body") or "{}")
    except json.JSONDecodeError:
        return {}


def get_user_id(event: dict) -> str | None:
    """
    Extract userId from the request headers.
    In a real app this would come from a JWT/Cognito authorizer.
    For this portfolio project we pass it as a header: X-User-Id
    """
    headers = event.get("headers") or {}
    # API Gateway lowercases header names
    return headers.get("x-user-id") or headers.get("X-User-Id")


def get_path_param(event: dict, param: str) -> str | None:
    """Extract a path parameter from the API Gateway event."""
    params = event.get("pathParameters") or {}
    return params.get(param)
