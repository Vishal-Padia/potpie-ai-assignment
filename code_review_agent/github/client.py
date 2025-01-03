import requests
from github import Github
from typing import Dict, List
from github.PullRequest import PullRequest
from code_review_agent.config import Config
from code_review_agent.utils.diff_parser import parse_diff


class GitHubClient:
    def __init__(self):
        self.github = Github(Config.GITHUB_TOKEN)

    def get_pull_request(self, repo_name: str, pr_number: int) -> PullRequest:
        """
        Fetch a pull request by repository name and PR number.
        """
        repo = self.github.get_repo(repo_name)
        return repo.get_pull(pr_number)

    def get_pr_diff(self, repo_name: str, pr_number: int) -> str:
        """
        Fetch the raw diff for a pull request.
        """
        pr = self.get_pull_request(repo_name, pr_number)
        headers = {"Authorization": f"token {Config.GITHUB_TOKEN}"}
        response = requests.get(pr.diff_url, headers=headers)
        response.raise_for_status()
        return response.text

    def get_parsed_diff(self, repo_name: str, pr_number: int) -> Dict[str, List[str]]:
        """
        Fetch and parse the diff for a pull request.
        """
        diff_text = self.get_pr_diff(repo_name, pr_number)
        return parse_diff(diff_text)
