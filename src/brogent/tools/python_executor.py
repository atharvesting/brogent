import sys
import subprocess as sp
from brogent.tools.core import subprocess_output, subprocess_output_specific

def execute_python(code: str, timeout_seconds: int = 10) -> dict:
    try:
        result = sp.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=timeout_seconds
        )

        return subprocess_output(result)

    except sp.TimeoutExpired:
        return subprocess_output_specific(
            False,
            "",
            f"Error: Code execution timed out after {timeout_seconds}.",
            -1
        )

