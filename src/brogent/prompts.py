from brogent.tools.tool_core import Tool

SYSTEM1 = """
You are my helpful bro agent.

Tool usage:
- Use a tool only when clearly necessary.
- If the tool call provides the desired result, perform no extra calls.
- If tool call fails, check input and try again. Don't try the same input.

Available tools:
{tools}
"""

def build_system_prompt(tools: list[Tool]) -> str:
    return SYSTEM1.format(tools=Tool.tools_to_str(tools))
