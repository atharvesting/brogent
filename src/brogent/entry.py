from brogent.agent import Brogent
from brogent.client import OllamaClient
from brogent.prompts import SYSTEM1
from brogent.tools import TOOLS

client = OllamaClient("qwen3:4b")
brogent = Brogent(client, system=SYSTEM1, tools=TOOLS)

question = ""

while question not in ("quit", "/q", "exit"):
    question = input("\n> ")
    print("\n==> ", end="")
    brogent.chat(question)

