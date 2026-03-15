"""
PUT /tasks/{taskId}
Updates an existing task. Only provided fields are updated (partial update).

Request body (all fields optional, at least one required):
  {
    "title":       "string",
    "description": "string",
    "status":      "TODO | IN_PROGRESS | DONE",
    "due_date":    "YYYY-MM-DD"
  }

Header:
  X-User-Id: <userId>
"""
import logging
import os
from datetime import datetime, timezone

import boto3
from botocore.exceptions import ClientError

from utils.helpers import error, get_path_param, get_user_id, parse_body, success

logger = logging.getLogger(__name__)

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

VALID_STATUSES = {"TODO", "IN_PROGRESS", "DONE"}
UPDATABLE_FIELDS = {"title", "description", "status", "due_date"}


def handler(event: dict, context) -> dict:
    logger.info("UpdateTask invoked")

    # ── Auth ──────────────────────────────
    user_id = get_user_id(event)
    if not user_id:
        return error("Missing required header: X-User-Id", 401)

    task_id = get_path_param(event, "taskId")
    if not task_id:
        return error("Missing path parameter: taskId")

    # ── Validate body ─────────────────────
    body = parse_body(event)
    updates = {k: v for k, v in body.items() if k in UPDATABLE_FIELDS}

    if not updates:
        return error(f"No valid fields to update. Allowed: {', '.join(UPDATABLE_FIELDS)}")

    if "status" in updates:
        updates["status"] = updates["status"].upper()
        if updates["status"] not in VALID_STATUSES:
            return error(f"'status' must be one of: {', '.join(VALID_STATUSES)}")

    if "title" in updates and not updates["title"].strip():
        return error("'title' cannot be empty")

    # ── Build DynamoDB update expression ──
    updates["updatedAt"] = datetime.now(timezone.utc).isoformat()

    update_expr_parts = []
    expr_attr_names = {}
    expr_attr_values = {}

    for i, (field, value) in enumerate(updates.items()):
        placeholder_name = f"#f{i}"
        placeholder_val  = f":v{i}"
        update_expr_parts.append(f"{placeholder_name} = {placeholder_val}")
        expr_attr_names[placeholder_name] = field
        expr_attr_values[placeholder_val]  = value

    update_expression = "SET " + ", ".join(update_expr_parts)

    # ── Persist ───────────────────────────
    try:
        response = table.update_item(
            Key={"userId": user_id, "taskId": task_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expr_attr_names,
            ExpressionAttributeValues=expr_attr_values,
            # Ensure the task exists before updating
            ConditionExpression="attribute_exists(taskId)",
            ReturnValues="ALL_NEW",
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return error(f"Task '{task_id}' not found", 404)
        raise

    updated_task = response.get("Attributes", {})
    logger.info("Updated task %s for user %s", task_id, user_id)
    return success({"message": "Task updated", "task": updated_task})
