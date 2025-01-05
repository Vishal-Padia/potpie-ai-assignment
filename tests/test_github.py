import pytest
from unittest.mock import patch, MagicMock
from code_review_agent.github.client import GitHubClient


@pytest.fixture
def github_client():
    return GitHubClient()


def test_get_pull_request(github_client):
    with patch("github.Github.get_repo") as mock_get_repo:
        mock_repo = MagicMock()
        mock_repo.get_pull.return_value = MagicMock()
        mock_get_repo.return_value = mock_repo

        pr = github_client.get_pull_request("owner/repo", 1)
        assert pr is not None
        mock_get_repo.assert_called_once_with("owner/repo")
        mock_repo.get_pull.assert_called_once_with(1)


def test_get_pr_diff(github_client):
    with patch("github.PullRequest.PullRequest.diff") as mock_diff:
        mock_diff.return_value = b"mock diff content"

        diff = github_client.get_pr_diff("owner/repo", 1)
        assert diff == "mock diff content"
        mock_diff.assert_called_once()


def test_get_parsed_diff(github_client):
    with patch(
        "code_review_agent.github.client.GitHubClient.get_pr_diff"
    ) as mock_get_pr_diff:
        mock_get_pr_diff.return_value = """
        diff --git a/file.txt b/file.txt
        index 1234567..89abcde 100644
        --- a/file.txt
        +++ b/file.txt
        @@ -1,5 +1,5 @@
        -old content
        +new content
        """

        parsed_diff = github_client.get_parsed_diff("owner/repo", 1)
        assert parsed_diff == {
            "file.txt": [
                {
                    "hunk_header": "@@ -1,5 +1,5 @@",
                    "start_old": 1,
                    "start_new": 1,
                    "changes": [
                        {
                            "type": "removed",
                            "content": "old content",
                            "line_old": 1,
                            "line_new": None,
                        },
                        {
                            "type": "added",
                            "content": "new content",
                            "line_old": None,
                            "line_new": 1,
                        },
                    ],
                }
            ]
        }
