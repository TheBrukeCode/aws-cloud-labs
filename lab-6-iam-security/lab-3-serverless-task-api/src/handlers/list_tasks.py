"""
GET /tasks
Lists all tasks for the authenticated user.
Supports optional filtering by status via query param: ?status=TODO

Header:
  X-User-Id: <userId>

Query Params (optional):
  status: TODO | IN_PROGRESS | DONE
"""
import logging
import os

import boto3
from boto3.dynamodb.conditions import Attr, Key

from utils.helpers import error, get_user_id, success

logger = logging.getLogger(__name__)

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

VALID_STATUSES = {"TODO", "IN_PROGRESS", "DONE"}


def handler(event: dict, context) -> dict:
    logger.info("ListTasks invoked")

    # ── Auth ──────────────────────────────
    user_id = get_user_id(event)
    if not user_id:
        return error("Missing required header: X-User-Id", 401)

    # ── Optional status filter ────────────
    query_params = event.get("queryStringParameters") or {}
    status_filter = query_params.get("status", "").upper() or None

    if status_filter and status_filter not in VALID_STATUSES:
        return error(f"'status' must be one of: {', '.join(VALID_STATUSES)}")

    # ── Query DynamoDB ────────────────────
    query_kwargs = {
        "KeyConditionExpression": Key("userId").eq(user_id)
    }

    if status_filter:
        query_kwargs["FilterExpression"] = Attr("status").eq(status_filter)

    response = table.query(**query_kwargs)
    tasks = response.get("Items", [])

    # Handle DynamoDB pagination (for large datasets)
    while "LastEvaluatedKey" in response:
        query_kwargs["ExclusiveStartKey"] = response["LastEvaluatedKey"]
        response = table.query(**query_kwargs)
        tasks.extend(response.get("Items", []))

    logger.info("Returning %d tasks for user %s", len(tasks), user_id)
    return success({"count": len(tasks), "tasks": tasks})
