from typing import Dict, Any
from code_review_agent.celery_app.celery import celery_app
from code_review_agent.agents.workflow import CodeReviewWorkflow
from code_review_agent.github.client import GitHubClient

# Initialize the workflow and GitHub client
review_workflow = CodeReviewWorkflow()
github_client = GitHubClient()


@celery_app.task
def review_pr_task(repo_name: str, pr_number: int) -> Dict[str, Any]:
    """
    Celery task to review a pull request.
    """
    try:
        # Fetch and parse the diff
        parsed_diff = github_client.get_parsed_diff(repo_name, pr_number)
        # Run the workflow with the parsed diff
        result = review_workflow.run(parsed_diff)
        return result
    except Exception as e:
        raise e
