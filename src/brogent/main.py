from brogent.agent import Brogent
from brogent.tools import TOOLS, TOOL_LIST
from brogent.prompts import build_system_prompt
from brogent.client import OllamaClient

if __name__ == "__main__":
    client = OllamaClient("qwen3:4b")
    bro = Brogent(client, build_system_prompt(TOOL_LIST), TOOLS)
    bro.start()
