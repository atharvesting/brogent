from typing import TypedDict, Callable
from abc import ABC

class ToolResult(TypedDict):
    success: bool
    stdout: str
    stderr: str
    exit_code: int

class Tool(ABC):
    def __init__(self, name: str, description: str, func: Callable, arguments: list):
        self.name = name
        self.description = description
        self.func = func
        self.arguments = arguments

    def __call__(self, *args, **kwargs) -> ToolResult:
        return self.func(*args, **kwargs)

    @staticmethod
    def tools_to_str(tools: list["Tool"]) -> str:
        r = ""
        for t in tools:
            args_str = ", ".join([
                f"{arg_name}: {arg_type}" for arg_name, arg_type in t.arguments
            ])

            r += f"{t.name}: Description: {t.description}, Arguments: {{{args_str}}}\n"

        return r

class Result:
    def success(stdout: str) -> ToolResult:
        return {
            "success": True,
            "stdout": stdout,
            "stderr": "",
            "exit_code": 0
        }

    def fail(stderr: str, exit_code: int = 1) -> ToolResult:
        return {
            "success": False,
            "stdout": "",
            "stderr": stderr,
            "exit_code": exit_code
        }
