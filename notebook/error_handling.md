- When sending a request to Ollama in order to generate an LLM response from its API,
there are different kinds of exceptions one can encounter:
    - Connection errors:
        - If the Ollama daemon isn't running in the background.
        - The selected port is not the correct one.
    - Timeout errors
    - Model availability:
        - Rate limited (429)
        - Unauthorized access
        - Model hasn't been pulled/installed yet (404).
    - Hardware errors:
        - Out of Memory
        - Unsupported architectures
    - Bad request errors (400)
    - More about Ollama API-specific exceptions here - https://github.com/ollama/ollama/blob/main/docs/api/errors.mdx

- Errors can occur at any stage of the program. As a rule of thumb, if a line of code exists, then there is probably
at least one way it can break.

