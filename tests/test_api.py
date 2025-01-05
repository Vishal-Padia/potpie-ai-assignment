import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from code_review_agent.api.endpoints import app


@pytest.fixture
def test_client():
    return TestClient(app)


def test_review_pr_endpoint(test_client):
    with patch("code_review_agent.api.endpoints.review_pr_task.delay") as mock_task:
        mock_task.return_value = MagicMock(id="mock-task-id")

        response = test_client.post("/pr/owner/repo/1/review")
        assert response.status_code == 200
        assert response.json() == {"task_id": "mock-task-id"}
        mock_task.assert_called_once_with("owner/repo", 1)


def test_get_task_status_endpoint(test_client):
    with patch("celery.result.AsyncResult") as mock_async_result:
        mock_result = MagicMock()
        mock_result.status = "SUCCESS"
        mock_result.result = {"feedback": []}
        mock_async_result.return_value = mock_result

        response = test_client.get("/task/mock-task-id")
        assert response.status_code == 200
        assert response.json() == {
            "task_id": "mock-task-id",
            "status": "SUCCESS",
            "result": {"feedback": []},
        }
