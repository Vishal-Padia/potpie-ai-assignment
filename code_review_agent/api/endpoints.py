import os
from huggingface_hub import login
from fastapi import FastAPI, HTTPException
from code_review_agent.github.client import GitHubClient
from code_review_agent.agents.workflow import CodeReviewWorkflow
from code_review_agent.utils.logging import setup_logging

# Initialize logging
setup_logging()

app = FastAPI()


# Hugging Face Login Prompt
def huggingface_login():
    if not os.getenv("HUGGINGFACE_TOKEN"):
        print("Hugging Face login is required to access the StarCoder model.")
        token = input("Enter your Hugging Face access token: ")
        os.environ["HUGGINGFACE_TOKEN"] = token
    login(token=os.getenv("HUGGINGFACE_TOKEN"))


# Run Hugging Face login when the app starts
huggingface_login()


github_client = GitHubClient()
review_workflow = CodeReviewWorkflow()


@app.get("/")
def read_root():
    return {"message": "Autonomous Code Review Agent"}


@app.post("/pr/{username}/{repo}/{pr_number}/review")
def review_pr(username: str, repo: str, pr_number: int):
    repo_name = f"{username}/{repo}"
    try:
        # Fetch and parse the diff
        parsed_diff = github_client.get_parsed_diff(repo_name, pr_number)
        # Run the workflow with the parsed diff
        result = review_workflow.run(parsed_diff)
        return result  # Return the feedback
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
