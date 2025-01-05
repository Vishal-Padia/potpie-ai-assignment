from typing import Dict, List, Any
import re


def parse_diff(diff_text: str) -> Dict[str, str]:
    """
    Parse a GitHub diff and return a dictionary of files with their full diff content.
    """
    files = {}
    current_file = None
    current_diff = []

    for line in diff_text.splitlines():
        # Check for file headers
        if line.startswith("diff --git"):
            if current_file:
                # Save the previous file's diff
                files[current_file] = "\n".join(current_diff)
                current_diff = []
            current_file = line.split(" ")[2][2:]  # Extract the file path
        # Capture all lines for the current file
        current_diff.append(line)

    # Save the last file's diff
    if current_file:
        files[current_file] = "\n".join(current_diff)

    return files
