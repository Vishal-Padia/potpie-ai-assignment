import pytest
from unittest.mock import patch, MagicMock
from code_review_agent.agents.workflow import CodeReviewWorkflow


@pytest.fixture
def review_workflow():
    return CodeReviewWorkflow()


def test_analyze_code(review_workflow):
    with patch(
        "code_review_agent.agents.tools.LLMCodeAnalyzer.analyze_code"
    ) as mock_analyze_code:
        mock_analyze_code.return_value = "mock feedback"

        diff = {
            "file.txt": [
                {
                    "hunk_header": "@@ -1,5 +1,5 @@",
                    "start_old": 1,
                    "start_new": 1,
                    "changes": [
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

        result = review_workflow.analyze_code(diff)
        assert result == {"analysis_results": {"file.txt": {1: "mock feedback"}}}


def test_generate_feedback(review_workflow):
    analysis_results = {"file.txt": {1: "mock feedback"}}

    feedback = review_workflow.generate_feedback(analysis_results)
    assert feedback == {
        "feedback": [
            {
                "file_path": "file.txt",
                "issues": [{"line_number": 1, "feedback": "mock feedback"}],
            }
        ]
    }
