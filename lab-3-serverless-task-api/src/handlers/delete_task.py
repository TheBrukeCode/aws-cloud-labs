"""
DELETE /tasks/{taskId}
Deletes a task for the authenticated user.

Header:
  X-User-Id: <userId>
"""
import logging
import os

import boto3
from botocore.exceptions import ClientError

from utils.helpers import error, get_path_param, get_user_id, success

logger = logging.getLogger(__name__)

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def handler(event: dict, context) -> dict:
    logger.info("DeleteTask invoked")

    # ── Auth ──────────────────────────────
    user_id = get_user_id(event)
    if not user_id:
        return error("Missing required header: X-User-Id", 401)

    task_id = get_path_param(event, "taskId")
    if not task_id:
        return error("Missing path parameter: taskId")

    # ── Delete from DynamoDB ──────────────
    try:
        table.delete_item(
            Key={"userId": user_id, "taskId": task_id},
            # Ensure the item exists before deleting
            ConditionExpression="attribute_exists(taskId)",
        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            return error(f"Task '{task_id}' not found", 404)
        raise

    logger.info("Deleted task %s for user %s", task_id, user_id)
    return success({"message": f"Task '{task_id}' deleted successfully"})
