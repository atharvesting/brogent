# Brogent - An experiment and initial dive into AI agents (without frameworks)

Features implemented:
- Tools (python execution, filesystem)
- Max-step cap
- Error recovery and feedback
- Trace logging

To be implemented:
- Evaluation cases + scoring
- Clearer and stricter orchestration
- Web search tool

---

### A Key Constraint: Use ollama's generate API as opposed to the chat API.

The chat API abstracts a lot of features we normally take for granted, such as support for tools, automatic
chat templates based on the model used, and context management. I wanted to focus on these details by building
them myself. Not trying to reinvent the wheel, but making sure that I get what goes on under the hood.

---

See [notebook](notebook/journey.md) for raw notes on experiments

PS - I have already built a simple agent like this [before](https://github.com/atharvesting/mini-projects/tree/main/2026-05_Rudimentary_AI_Agent).
This project focuses on understanding how the model behaves under the harness, what a harness needs to be effective,
and an iterative process of improving overall performance.
