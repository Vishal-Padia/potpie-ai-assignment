from transformers import AutoTokenizer, AutoModelForCausalLM


class LLMCodeAnalyzer:
    def __init__(self, model_name: str = ""):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

    def analyze_code(self, code: str) -> str:
        """
        Analyze code using an LLM and return feedback.
        """
        prompt = f"""
        Analyze the following code for quality, style, and best practices. Provide actionable feedback:
        ```python
        {code}
        ```
        Feedback:
        """
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_length=512)
        feedback = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return feedback
