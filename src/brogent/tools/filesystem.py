import subprocess as sp
from pathlib import Path
from brogent.tools.core import subprocess_output, subprocess_output_specific

allowed = ["ls", "cat", "touch", "cwd"]

def file_operation(command: str, path_boundary: str | None = None):
    if path_boundary is None:
        path_boundary = Path.cwd()
    parent = Path(path_boundary).resolve()
    divided = command.split(" ")
    target = Path(divided[-1]).resolve()

    if len(divided) == 1 and command.startswith(tuple(allowed)):
        pass

    elif not parent in target.parents or parent != target:
        return subprocess_output_specific(
            False,
            "",
            f"File location unauthorized. Command aborted. The target file must be within {parent}",
            1
        )

    elif not command.startswith(tuple(allowed)):
        return subprocess_output_specific(
            False,
            "",
            f"Unauthorized or incorrect command used for file I/O. Command aborted. Only " + ",".join(allowed), " are allowed to be performed.",
            1
        )

    result = sp.run(divided, capture_output=True, text=True)

    return subprocess_output(result)
