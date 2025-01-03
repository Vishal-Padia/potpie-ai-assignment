from langgraph import Agent
from typing import Dict, List, Any
from code_review_agent.agents.tools import (
    analyze_code_quality,
    check_code_style,
    enforce_best_practices,
)


class ReviewAgent(Agent):
    def __init__(self):
        super().__init__()
        self.tools = {
            "analyze_code_quality": analyze_code_quality,
            "check_code_style": check_code_style,
            "enforce_best_practices": enforce_best_practices,
        }

    def review_code(self, code: str) -> Dict[str, Dict[str, str]]:
        """
        Review code using all available tools.
        """
        results = {}
        for tool_name, tool_func in self.tools.items():
            results[tool_name] = tool_func(code)
        return results

    def review_diff(
        self, diff: Dict[str, List[Dict[str, Any]]]
    ) -> Dict[str, Dict[str, Dict[str, str]]]:
        """
        Review a parsed diff using all available tools.
        """
        results = {}
        for file_path, hunks in diff.items():
            file_results = {}
            for hunk in hunks:
                for change in hunk["changes"]:
                    if change["type"] in ("added", "removed"):
                        code = change["content"]
                        file_results[change["line_new"]] = self.review_code(code)
            results[file_path] = file_results
        return results
