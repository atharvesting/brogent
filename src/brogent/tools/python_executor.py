import sys
import subprocess as sp
from brogent.tools.tool_core import Tool, ToolResult, subprocess_output, subprocess_output_specific

def _execute_python(code: str, timeout_seconds: int = 10) -> ToolResult:
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

execute_python = Tool(
    name="execute_python",
    description="Run deterministic python code and return its output",
    func=_execute_python,
    arguments=[
        ("code", "str"),
        ("timeout_seconds", "int")
    ]
)
