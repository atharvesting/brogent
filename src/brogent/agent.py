from brogent.client import OllamaClient, Response
from pydantic import ValidationError
import json
import pathlib
from datetime import datetime

MAX_STEPS = 5

class Memory:
    def __init__(self, system: str):
        self.messages = [{"role": "system", "content": system}]
        timestamp = datetime.now().strftime("%Y-%m-%d-%Hh%Mm")
        chat_id = f"bro-{timestamp}.json"
        self.trace_path = pathlib.Path("traces") / chat_id
        self.trace_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.trace_path, "w") as t:
            json.dump(self.messages, t, indent=4)

    def _get_messages(self):
            messages = ""
            for mesdic in self.messages:
                messages += mesdic["role"] + ": " + str(mesdic["content"]) + "\n"

            return messages

    def _append(self, role: str, content: str) -> None:
        self.messages.append({"role": role, "content": content})
        self._update()

    def _update(self):
        with open(self.trace_path, "w") as t:
            t.write(json.dumps(self.messages, indent=4))

class Brogent:
    def __init__(self, api: OllamaClient, system: str, tools: dict):
        self.api = api
        self.system = system
        self.memory = Memory(system)
        self.tools = tools

    def chat(self, message: str) -> None:

        self.memory._append("user", message)

        for _ in range(MAX_STEPS):
            full_response = self.api.generate(self.memory._get_messages())
            raw = full_response.response
            response = self.parse_response(raw)
            response.thought = full_response.thinking

            if not response:
                print("Exception: Structured output failure. Try asking again!")
                return

            self.memory._append("assistant", response.model_dump_json())

            if response.kind == "final":
                print(response.answer)
                return

            if response.tool is None:
                self.memory._append("tool", "Error: kind='tool' but no tool call was provided. Reply with kind='final'.")
                continue

            if response.tool.tool_name in self.tools:
                result = self.tools[response.tool.tool_name](**response.tool.tool_arguments)
                self.memory._append("tool", json.dumps(result))
            else:
                self.memory._append("tool", f"The tool {response.tool.tool_name} does not exist")

        print(f"[stopped: hit MAX_STEPS={MAX_STEPS} without a final answer]")

    def parse_response(self, response: str) -> Response | None:
        try:
            validated = Response.model_validate_json(response)
            return validated

        except ValidationError as e:
            print("Model response did not conform to predefined structure.")
            print("Cannot reliably proceed with the task.")
            return None




