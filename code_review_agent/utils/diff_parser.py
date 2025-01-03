from typing import Dict, List, Any
import re


def parse_diff(diff_text: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Parse a GitHub diff and return a structured representation of changes.

    Args:
        diff_text (str): The raw diff text from GitHub.

    Returns:
        Dict[str, List[Dict[str, Any]]]: A dictionary where keys are file paths and values are lists of changes.
    """
    files = {}
    current_file = None
    current_hunk = None

    for line in diff_text.splitlines():
        # Check for file headers
        if line.startswith("diff --git"):
            current_file = line.split(" ")[2][2:]  # Extract the file path
            files[current_file] = []
        # Check for hunk headers
        elif line.startswith("@@"):
            if current_file:
                # Extract line numbers from the hunk header
                line_numbers = re.search(r"@@ -(\d+),\d+ \+(\d+),\d+ @@", line)
                if line_numbers:
                    start_old = int(line_numbers.group(1))
                    start_new = int(line_numbers.group(2))
                    current_hunk = {
                        "hunk_header": line,
                        "start_old": start_old,
                        "start_new": start_new,
                        "changes": [],
                    }
                    files[current_file].append(current_hunk)
        # Capture changes
        elif line.startswith(("+", "-", " ")):
            if current_file and current_hunk:
                change_type = (
                    "added"
                    if line.startswith("+")
                    else "removed" if line.startswith("-") else "context"
                )
                current_hunk["changes"].append(
                    {
                        "type": change_type,
                        "content": line[1:],  # Remove the +, -, or space
                        "line_old": (
                            start_old if change_type in ("removed", "context") else None
                        ),
                        "line_new": (
                            start_new if change_type in ("added", "context") else None
                        ),
                    }
                )
                # Update line numbers
                if change_type in ("removed", "context"):
                    start_old += 1
                if change_type in ("added", "context"):
                    start_new += 1

    return files
