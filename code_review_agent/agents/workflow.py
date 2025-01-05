from typing import Dict, Any
from code_review_agent.agents.tools import LLMCodeAnalyzer


class CodeReviewWorkflow:
    def __init__(self):
        self.llm_analyzer = LLMCodeAnalyzer()

    def analyze_code(self, diff: Dict[str, str]) -> Dict[str, Any]:
        """
        Analyze the code using the LLM.
        """
        analysis_results = {}

        for file_path, file_diff in diff.items():
            feedback = self.llm_analyzer.analyze_code(file_diff)
            analysis_results[file_path] = feedback

        return {"analysis_results": analysis_results}

    def generate_feedback(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate structured feedback based on the analysis results.
        """
        feedback = []

        for file_path, feedback_data in analysis_results.items():
            file_feedback = {
                "file_path": file_path,
                "code_quality": feedback_data["code_quality"],
                "code_style": feedback_data["code_style"],
                "best_practices": feedback_data["best_practices"],
                "suggestions": feedback_data["suggestions"],
            }
            feedback.append(file_feedback)

        return {"feedback": feedback}

    def run(self, diff: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the workflow for a given parsed diff.
        """
        # Step 1: Analyze the code
        analysis_results = self.analyze_code(diff)
        # Step 2: Generate feedback
        feedback = self.generate_feedback(analysis_results["analysis_results"])
        return feedback
