"""
Unit tests for the Serverless Task API handlers.
Run with: pytest tests/ -v
"""
import json
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Allow imports from src/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
os.environ["TABLE_NAME"] = "tasks-test"

from handlers import create_task, delete_task, get_task, list_tasks, update_task


def make_event(method="GET", body=None, path_params=None, query_params=None, user_id="user-123"):
    """Helper to build a mock API Gateway event."""
    return {
        "httpMethod": method,
        "headers": {"x-user-id": user_id},
        "pathParameters": path_params or {},
        "queryStringParameters": query_params or {},
        "body": json.dumps(body) if body else None,
    }


class TestCreateTask(unittest.TestCase):

    @patch("handlers.create_task.table")
    def test_create_task_success(self, mock_table):
        mock_table.put_item.return_value = {}
        event = make_event("POST", body={"title": "Buy groceries", "status": "TODO"})
        response = create_task.handler(event, None)

        self.assertEqual(response["statusCode"], 201)
        body = json.loads(response["body"])
        self.assertEqual(body["task"]["title"], "Buy groceries")
        self.assertEqual(body["task"]["status"], "TODO")

    def test_create_task_missing_user_id(self):
        event = make_event("POST", body={"title": "Test"}, user_id=None)
        event["headers"] = {}
        response = create_task.handler(event, None)
        self.assertEqual(response["statusCode"], 401)

    def test_create_task_missing_title(self):
        event = make_event("POST", body={"description": "No title here"})
        response = create_task.handler(event, None)
        self.assertEqual(response["statusCode"], 400)

    def test_create_task_invalid_status(self):
        event = make_event("POST", body={"title": "Test", "status": "INVALID"})
        response = create_task.handler(event, None)
        self.assertEqual(response["statusCode"], 400)


class TestGetTask(unittest.TestCase):

    @patch("handlers.get_task.table")
    def test_get_task_success(self, mock_table):
        mock_table.get_item.return_value = {
            "Item": {"userId": "user-123", "taskId": "abc-123", "title": "Test Task"}
        }
        event = make_event("GET", path_params={"taskId": "abc-123"})
        response = get_task.handler(event, None)

        self.assertEqual(response["statusCode"], 200)
        body = json.loads(response["body"])
        self.assertEqual(body["task"]["taskId"], "abc-123")

    @patch("handlers.get_task.table")
    def test_get_task_not_found(self, mock_table):
        mock_table.get_item.return_value = {}
        event = make_event("GET", path_params={"taskId": "nonexistent"})
        response = get_task.handler(event, None)
        self.assertEqual(response["statusCode"], 404)


class TestListTasks(unittest.TestCase):

    @patch("handlers.list_tasks.table")
    def test_list_tasks_success(self, mock_table):
        mock_table.query.return_value = {
            "Items": [
                {"taskId": "1", "title": "Task 1", "status": "TODO"},
                {"taskId": "2", "title": "Task 2", "status": "DONE"},
            ]
        }
        event = make_event("GET")
        response = list_tasks.handler(event, None)

        self.assertEqual(response["statusCode"], 200)
        body = json.loads(response["body"])
        self.assertEqual(body["count"], 2)

    @patch("handlers.list_tasks.table")
    def test_list_tasks_with_status_filter(self, mock_table):
        mock_table.query.return_value = {
            "Items": [{"taskId": "1", "title": "Task 1", "status": "TODO"}]
        }
        event = make_event("GET", query_params={"status": "TODO"})
        response = list_tasks.handler(event, None)
        self.assertEqual(response["statusCode"], 200)

    def test_list_tasks_invalid_status(self):
        event = make_event("GET", query_params={"status": "GARBAGE"})
        response = list_tasks.handler(event, None)
        self.assertEqual(response["statusCode"], 400)


class TestUpdateTask(unittest.TestCase):

    @patch("handlers.update_task.table")
    def test_update_task_success(self, mock_table):
        mock_table.update_item.return_value = {
            "Attributes": {"taskId": "abc-123", "title": "Updated", "status": "DONE"}
        }
        event = make_event("PUT", body={"status": "DONE"}, path_params={"taskId": "abc-123"})
        response = update_task.handler(event, None)
        self.assertEqual(response["statusCode"], 200)

    def test_update_task_no_valid_fields(self):
        event = make_event("PUT", body={"unknown_field": "value"}, path_params={"taskId": "abc"})
        response = update_task.handler(event, None)
        self.assertEqual(response["statusCode"], 400)


class TestDeleteTask(unittest.TestCase):

    @patch("handlers.delete_task.table")
    def test_delete_task_success(self, mock_table):
        mock_table.delete_item.return_value = {}
        event = make_event("DELETE", path_params={"taskId": "abc-123"})
        response = delete_task.handler(event, None)
        self.assertEqual(response["statusCode"], 200)
        body = json.loads(response["body"])
        self.assertIn("deleted", body["message"])

    def test_delete_task_missing_id(self):
        event = make_event("DELETE", path_params={})
        response = delete_task.handler(event, None)
        self.assertEqual(response["statusCode"], 400)


if __name__ == "__main__":
    unittest.main()
