from langgraph.graph import Graph
from typing import Dict, Any
from code_review_agent.agents.tools import LLMCodeAnalyzer


class CodeReviewWorkflow:
    def __init__(self):
        self.llm_analyzer = LLMCodeAnalyzer()
        self.workflow = Graph()

        # Define the workflow steps
        self.workflow.add_node("analyze_code", self.analyze_code)
        self.workflow.add_node("generate_feedback", self.generate_feedback)

        # Define the edges
        self.workflow.add_edge("analyze_code", "generate_feedback")

        # Set the entry point
        self.workflow.set_entry_point("analyze_code")

    def analyze_code(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the code using the LLM.
        """
        diff = state["diff"]
        analysis_results = {}

        for file_path, hunks in diff.items():
            file_results = {}
            for hunk in hunks:
                for change in hunk["changes"]:
                    if change["type"] in ("added", "removed"):
                        code = change["content"]
                        feedback = self.llm_analyzer.analyze_code(code)
                        file_results[change["line_new"]] = feedback
            analysis_results[file_path] = file_results

        return {"analysis_results": analysis_results}

    def generate_feedback(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate feedback based on the analysis results.
        """
        analysis_results = state["analysis_results"]
        feedback = []

        for file_path, changes in analysis_results.items():
            file_feedback = {"file_path": file_path, "issues": []}
            for line_number, feedback_text in changes.items():
                file_feedback["issues"].append(
                    {"line_number": line_number, "feedback": feedback_text}
                )
            if file_feedback["issues"]:
                feedback.append(file_feedback)

        return {"feedback": feedback}

    def run(self, diff: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the workflow for a given parsed diff.
        """
        initial_state = {"diff": diff}
        return self.workflow.run(initial_state)
