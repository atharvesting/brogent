import ollama
from pydantic import BaseModel
from typing import Literal

class ToolCall(BaseModel):
    tool_name: str
    tool_arguments: dict

class Response(BaseModel):
    thought: str = ""
    kind: Literal["tool", "final"]
    tool: ToolCall | None = None
    answer: str | None = None

class OllamaClient():
    def __init__(self, model: str):
        self.model = model

    def chat(self, messages: list[dict]):
        try:
            response = ollama.chat(
                model=self.model,
                messages=messages,
                keep_alive="1h",
                think=True,
                format=Response.model_json_schema(),
                options={
                    "temperature": 0.25
                }
            )
            return response

        except ollama.ResponseError as e:
            if e.status_code == 404:
                print(f"Error: Model '{self.model}' not installed locally. Run 'ollama pull {self.model}'.")
            else:
                print(f"Ollama Server Error [{e.status_code}]: {e.error}")

        except Exception as e:
            print(f"Failed to connect to Ollama: {e}")

        return None

    @staticmethod
    def to_chat_template(messages: list[dict]) -> str:
        final = ""
        for m in messages:
            final += "<|im_start|>" + m["role"] + "\n"
            final += m["content"] + "\n"
            final += "<|im_end|>\n"
        final += "<|im_start|>assistant\n"
        return final
