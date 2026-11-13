import sys
import subprocess as sp
from brogent.tools.tool_core import Tool, ToolResult, Result

def _execute_python(code: str, timeout_seconds: int = 10) -> ToolResult:
    try:
        result = sp.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=timeout_seconds
        )
        if result.returncode != 0:
            return Result.fail("Faulty Python Code: " + result.stderr, result.returncode)

        return Result.success(result.stdout)

    except sp.TimeoutExpired:
        return Result.fail(f"Error: Code execution timed out after {timeout_seconds}.", -1)

execute_python = Tool(
    name="execute_python",
    description="Run deterministic python code and return its output",
    func=_execute_python,
    arguments=[
        ("code", "str"),
        ("timeout_seconds", "int")
    ]
)
