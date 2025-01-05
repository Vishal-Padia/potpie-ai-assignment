import pytest
from fastapi.testclient import TestClient
from code_review_agent.api.endpoints import app
from code_review_agent.github.client import GitHubClient
from code_review_agent.agents.workflow import CodeReviewWorkflow


@pytest.fixture
def test_client():
    """
    Fixture to provide a test client for the FastAPI app.
    """
    return TestClient(app)


@pytest.fixture
def mock_github_client():
    """
    Fixture to provide a mock GitHub client.
    """
    return GitHubClient()


@pytest.fixture
def mock_review_workflow():
    """
    Fixture to provide a mock CodeReviewWorkflow.
    """
    return CodeReviewWorkflow()
