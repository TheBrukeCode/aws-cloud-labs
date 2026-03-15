"""
POST /tasks
Creates a new task for a user.

Request body:
  {
    "title":       "string (required)",
    "description": "string (optional)",
    "status":      "TODO | IN_PROGRESS | DONE (optional, default: TODO)",
    "due_date":    "YYYY-MM-DD (optional)"
  }

Header:
  X-User-Id: <userId>
"""
import logging
import os
import uuid
from datetime import datetime, timezone

import boto3

from utils.helpers import error, get_user_id, parse_body, success

logger = logging.getLogger(__name__)

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

VALID_STATUSES = {"TODO", "IN_PROGRESS", "DONE"}


def handler(event: dict, context) -> dict:
    logger.info("CreateTask invoked")

    # ── Auth ──────────────────────────────
    user_id = get_user_id(event)
    if not user_id:
        return error("Missing required header: X-User-Id", 401)

    # ── Validate body ─────────────────────
    body = parse_body(event)
    title = body.get("title", "").strip()
    if not title:
        return error("'title' is required and cannot be empty")

    status = body.get("status", "TODO").upper()
    if status not in VALID_STATUSES:
        return error(f"'status' must be one of: {', '.join(VALID_STATUSES)}")

    # ── Build item ────────────────────────
    task_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()

    item = {
        "userId":      user_id,
        "taskId":      task_id,
        "title":       title,
        "status":      status,
        "createdAt":   now,
        "updatedAt":   now,
    }

    if body.get("description"):
        item["description"] = body["description"].strip()

    if body.get("due_date"):
        item["due_date"] = body["due_date"]

    # ── Persist ───────────────────────────
    table.put_item(Item=item)
    logger.info("Created task %s for user %s", task_id, user_id)

    return success({"message": "Task created", "task": item}, status_code=201)
