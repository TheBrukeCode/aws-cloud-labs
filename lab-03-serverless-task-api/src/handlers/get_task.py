"""
GET /tasks/{taskId}
Fetches a single task by ID for the authenticated user.

Header:
  X-User-Id: <userId>
"""
import logging
import os

import boto3
from boto3.dynamodb.conditions import Key

from utils.helpers import error, get_path_param, get_user_id, success

logger = logging.getLogger(__name__)

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def handler(event: dict, context) -> dict:
    logger.info("GetTask invoked")

    # ── Auth ──────────────────────────────
    user_id = get_user_id(event)
    if not user_id:
        return error("Missing required header: X-User-Id", 401)

    task_id = get_path_param(event, "taskId")
    if not task_id:
        return error("Missing path parameter: taskId")

    # ── Fetch from DynamoDB ───────────────
    response = table.get_item(
        Key={"userId": user_id, "taskId": task_id}
    )

    task = response.get("Item")
    if not task:
        return error(f"Task '{task_id}' not found", 404)

    return success({"task": task})
