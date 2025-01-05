# potpie-ai-assignment

Assignment Link: https://potpieai.notion.site/Founding-Engineer-Backend-Take-Home-Assignment-139c13a23aa880a1a3edfb5c150db847

# Autonomous Code Review Agent

An autonomous code review agent that analyzes pull requests using Large Language Models (LLMs). This project integrates with GitHub to fetch pull request diffs, analyzes the code changes using an LLM (e.g., StarCoder or GPT-2), and provides actionable feedback.

## Prerequisites
- Python 3.9 or higher
- A GitHub account (optional, for accessing private repositories)
- A Hugging Face account (for accessing gated models like StarCoder)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Vishal-Padia/potpie-ai-assignment
   cd code-review-agent
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   - Create a `.env` file in the root directory:
     ```bash
     touch .env
     ```
   - Add the following variables to `.env`:
     ```text
     # GitHub Token (optional, for private repositories)
     GITHUB_TOKEN=your_github_token_here

     # Hugging Face Token (required for gated models like StarCoder)
     HUGGINGFACE_TOKEN=your_huggingface_token_here
     ```

## Running the Application

1. **Start the FastAPI Server**:
   ```bash
   uvicorn code_review_agent.api.endpoints:app --reload
   ```
   The server will start at `http://127.0.0.1:8000`.

2. **Test the API**:
   - Use `curl` or a tool like Postman to send requests to the API.
   - Example request to analyze a pull request:
     ```bash
     curl -X POST http://127.0.0.1:8000/pr/{user_name}/{repo_name}/{pr_number}/review
     ```
   - Example response:
     ```json
     {
       "feedback": [
         {
           "file_path": "README.md",
           "issues": [
             {
               "line_number": 2,
               "feedback": "The code looks good, but consider adding more comments for clarity."
             }
           ]
         }
       ]
     }
     ```

## Project Structure

```
code-review-agent/
├── code_review_agent/
│   ├── __init__.py
│   ├── config.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── tools.py
│   │   └── workflow.py
│   ├── github/
│   │   ├── __init__.py
│   │   └── client.py
│   └── utils/
│       ├── __init__.py
│       ├── logging.py
│       └── diff_parser.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api.py
│   ├── test_agents.py
│   └── test_github.py
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
```

## Configuration

### Environment Variables
- `GITHUB_TOKEN`: Your GitHub personal access token (required for private repositories).
- `HUGGINGFACE_TOKEN`: Your Hugging Face access token (required for gated models like StarCoder).

### Using a Different LLM
To use a different LLM (e.g., GPT-2), update the `LLMCodeAnalyzer` class in `code_review_agent/agents/tools.py`:
```python
class LLMCodeAnalyzer:
    def __init__(self, model_name: str = "gpt2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
```

## Troubleshooting

### Hugging Face Login Issues
If you encounter issues with Hugging Face authentication:
1. Ensure your `HUGGINGFACE_TOKEN` is correct.
2. Manually log in using the `huggingface-cli`:
   ```bash
   huggingface-cli login
   ```

### GitHub API Rate Limits
If you hit GitHub API rate limits:
1. Use a GitHub token by setting the `GITHUB_TOKEN` environment variable.
2. Authenticated requests have a higher rate limit (5,000 requests per hour).

### Model Loading Issues
If the LLM fails to load:
1. Ensure you have enough memory (RAM/GPU) for the model.
2. Use a smaller model (e.g., `gpt2` instead of `starcoder`).

---

## Future Enhancements
- Add support for more LLMs (e.g., CodeGen, GPT-Neo).
- Integrate with CI/CD pipelines for automated code reviews.
- Add a frontend for visualizing feedback.

