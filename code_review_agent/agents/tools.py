from typing import Dict, Any, List
from transformers import AutoTokenizer, AutoModelForCausalLM


class LLMCodeAnalyzer:
    def __init__(self, model_name: str = "bigcode/starcoderbase-1b"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name, use_auth_token=True
        )
        self.max_tokens = 2048  # Adjust based on the model's context window
        # Reserve tokens for the prompt template and model response
        self.reserved_tokens = (
            700  # Adjust based on your prompt length and desired output length
        )
        self.effective_max_tokens = self.max_tokens - self.reserved_tokens

    def analyze_code(self, diff: str) -> Dict[str, Any]:
        """
        Analyze the code diff in chunks and return structured feedback.
        """
        # Split the diff into chunks
        chunks = self._split_diff_into_chunks(diff)
        feedback = []

        for chunk in chunks:
            # Create the prompt
            prompt = self._create_analysis_prompt(chunk)

            # Tokenize the prompt
            inputs = self.tokenizer(prompt, return_tensors="pt")

            try:
                # Generate feedback with controlled output length
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=512,
                    pad_token_id=self.tokenizer.eos_token_id,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.95,
                )
                chunk_feedback = self.tokenizer.decode(
                    outputs[0], skip_special_tokens=True
                )
                feedback.append(self._parse_feedback(chunk_feedback))
            except Exception as e:
                print(f"Error processing chunk: {str(e)}")
                continue

        # Combine feedback from all chunks
        combined_feedback = self._combine_feedback(feedback)
        return combined_feedback

    def _create_analysis_prompt(self, chunk: str) -> str:
        """
        Create a prompt for code analysis with proper token management.
        """
        prompt_template = """
        Analyze the following code changes for quality, style, and best practices. Provide actionable feedback in the following format:
        - **Code Quality**: [Feedback on code quality, e.g., readability, maintainability]
        - **Code Style**: [Feedback on code style, e.g., adherence to PEP 8]
        - **Best Practices**: [Feedback on best practices, e.g., security, performance]
        - **Suggestions**: [Specific suggestions to improve the code, including code snippets if applicable]

        Diff:
        ```diff
        {chunk}
        ```

        Feedback:
        """
        return prompt_template.format(chunk=chunk)

    def _split_diff_into_chunks(self, diff: str) -> List[str]:
        """
        Split the diff into chunks that fit within the model's effective token limit.
        """
        lines = diff.splitlines()
        chunks = []
        current_chunk = []
        current_token_count = 0

        for line in lines:
            # Tokenize the current line
            line_tokens = self.tokenizer.encode(line, add_special_tokens=False)
            line_token_count = len(line_tokens)

            # Check if adding this line exceeds the effective token limit
            if current_token_count + line_token_count > self.effective_max_tokens:
                if current_chunk:  # Only add non-empty chunks
                    chunks.append("\n".join(current_chunk))
                current_chunk = []
                current_token_count = 0

                # Handle lines that are too long by themselves
                if line_token_count > self.effective_max_tokens:
                    # Split the line into smaller pieces
                    line_pieces = self._split_line(line)
                    for piece in line_pieces:
                        chunks.append(piece)
                else:
                    current_chunk = [line]
                    current_token_count = line_token_count
            else:
                current_chunk.append(line)
                current_token_count += line_token_count

        # Add the last chunk if it's not empty
        if current_chunk:
            chunks.append("\n".join(current_chunk))

        return chunks

    def _split_line(self, line: str) -> List[str]:
        """
        Split a single line into smaller pieces that fit within token limits.
        """
        tokens = self.tokenizer.encode(line, add_special_tokens=False)
        pieces = []
        for i in range(0, len(tokens), self.effective_max_tokens):
            piece_tokens = tokens[i : i + self.effective_max_tokens]
            piece = self.tokenizer.decode(piece_tokens)
            pieces.append(piece)
        return pieces

    def _combine_feedback(self, feedback: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Combine feedback from multiple chunks into a single response.
        Removes duplicates and maintains coherent narrative.
        """
        combined_feedback = {
            "code_quality": set(),
            "code_style": set(),
            "best_practices": set(),
            "suggestions": set(),
        }

        # Collect unique feedback items
        for chunk_feedback in feedback:
            for key in combined_feedback:
                if chunk_feedback[key]:
                    combined_feedback[key].add(chunk_feedback[key])

        # Convert sets to formatted strings
        return {
            key: "\n".join(f"- {item}" for item in items)
            for key, items in combined_feedback.items()
        }

    def _parse_feedback(self, feedback: str) -> Dict[str, Any]:
        """
        Parse the raw feedback into a structured format.
        Handle potential missing sections gracefully.
        """
        parsed_feedback = {
            "code_quality": "",
            "code_style": "",
            "best_practices": "",
            "suggestions": "",
        }

        try:
            # Extract feedback sections
            sections = feedback.split("**")
            for section in sections:
                for key in parsed_feedback:
                    if key.replace("_", " ").title() in section:
                        content = section.split(":", 1)
                        if len(content) > 1:
                            parsed_feedback[key] = content[1].strip()
        except Exception as e:
            print(f"Error parsing feedback: {str(e)}")

        return parsed_feedback
