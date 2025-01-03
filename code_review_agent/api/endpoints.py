from fastapi import FastAPI, HTTPException
from code_review_agent.github.client import GitHubClient
from code_review_agent.utils.logging import setup_logging
from code_review_agent.agents.review_agent import ReviewAgent
from code_review_agent.agents.workflow import CodeReviewWorkflow

# Initialize logging
setup_logging()

app = FastAPI(title="Code Review Agent")
github_client = GitHubClient()
review_agent = ReviewAgent()
workflow = CodeReviewWorkflow()


@app.get("/")
def read_root():
    return {"message": "Autonomous Code Review Agent"}


@app.post("/pr/{username}/{repo}/{pr_number}/review")
def review_pr(username: str, repo: str, pr_number: int):
    repo_name = f"{username}/{repo}"
    try:
        # Fetch and parse the diff
        parsed_diff = github_client.get_parsed_diff(repo_name, pr_number)
        # Review the diff using the agent
        review_results = review_agent.review_diff(parsed_diff)
        result = CodeReviewWorkflow.run_workflow(parsed_diff)
        return result["feedback"]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
