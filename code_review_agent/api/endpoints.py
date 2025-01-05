import os
from huggingface_hub import login
from celery.result import AsyncResult
from fastapi import FastAPI, HTTPException
from code_review_agent.github.client import GitHubClient
from code_review_agent.agents.workflow import CodeReviewWorkflow
from code_review_agent.utils.logging import setup_logging
from code_review_agent.celery_app.tasks import review_pr_task

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
        # Trigger the Celery task
        task = review_pr_task.delay(repo_name, pr_number)
        return {"task_id": task.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/status/{task_id}")
def get_task_status(task_id: str):
    """
    Check the status of a Celery task.
    """
    task_result = AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task_result.status,
    }


@app.get("/results/{task_id}")
def get_task_result(task_id: str):
    """
    Get the result for the task id
    """
    task_result = AsyncResult(task_id)
    return {
        "task_id": task_id,
        "result": task_result.result if task_result.ready() else None,
    }
