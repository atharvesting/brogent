from pathlib import Path
from brogent.tools.tool_core import Tool, ToolResult, Result
import tempfile
import os
import shutil
from functools import partial

ROOT_PATH = "/home/yolomofo/Desktop/Main/code/brogent/"

def _validate_and_resolve_path(root: Path, path_str: str) -> Path:
    target_path = Path(path_str)
    root = root.resolve(strict=True)

    if not target_path.is_absolute():
        target_path = root / target_path

    resolved_path = target_path.resolve()

    try:
        resolved_path.relative_to(root)
        return resolved_path
    except ValueError:
        raise PermissionError(f"{resolved_path} is outside allowed folder ({root}.)")

def _list_files(root: Path, directory_path: str) -> ToolResult:
    try:
        resolved_path = _validate_and_resolve_path(root, directory_path)
        if resolved_path.is_file():
            return Result.fail(f"{resolved_path} points to a file path. Make sure to use a directory path.")

        resolved_path.resolve(strict=True)
        files = "\n".join([f.name for f in resolved_path.iterdir() if f.is_file()])
        return Result.success(f"Files inside {resolved_path.name}:\n{files}")

    except Exception as e:
        return Result.fail(f"Error: List operation failed. Check arguments. {e}")


def _read_file(root: Path, file_path: str) -> ToolResult:
    try:
        resolved_path = _validate_and_resolve_path(root, file_path)
        content = Path.read_text(resolved_path)
        return Result.success(content)

    except Exception as e:
        return Result.fail(f"Error: Couldn't read file. {e}")


def _write_file(root: Path, file_path: str, content: str) -> ToolResult:
    try:
        resolved_path = _validate_and_resolve_path(root, file_path)

        if Path.exists(resolved_path):
            return Result.fail("Error: Path already exists. Cannot overwrite file. If available, use the edit tool instead.")

        resolved_path.parent.mkdir(parents=True, exist_ok=True)

        with open(resolved_path, "w", encoding="utf-8") as f:
            f.write(content)

        return Result.success(f"File {resolved_path} Written Successfully")

    except Exception as e:
        return Result.fail(f"Error: Couldn't write file. {e}")


def _delete_file(root: Path, file_path: str, reason: str) -> ToolResult:
    if not file_path:
        return Result.fail("No file path provided. Provide a valid file path, or abort action.")
    if not reason:
        return Result.fail(f"No reason provided for deleting '{file_path}'. Either provide a valid reason, or abort action.")

    try:
        resolved_path = _validate_and_resolve_path(root, file_path)
        resolved_path.unlink()
        return Result.success(f"File {resolved_path} successfully deleted.")

    except Exception as e:
        return Result.fail(f"Error: Couldn't delete file. {e}")

def _edit_file(root: Path,
               file_path: str | Path,
               old_string: str,
               new_string: str,
               replace_all: bool = False) -> ToolResult:
    if not isinstance(file_path, str | Path):
        return Result.fail("file_path must be a string or Path.")
    if isinstance(file_path, str) and not file_path.strip():
        return Result.fail("file_path must not be empty.")
    if not isinstance(old_string, str) or old_string == "":
        return Result.fail("old_string must be the exact text you want replaced, and cannot be empty.")
    if not isinstance(new_string, str):
        return Result.fail("new_string must be text (wrap it in quotes).")
    if old_string == new_string:
        return Result.fail("old_string and new_string are identical, so nothing will change.")
    if not isinstance(replace_all, bool):
        return Result.fail("replace_all must be a boolean value, without quotes")

    try:
        file = _validate_and_resolve_path(root, file_path)

        if not file.exists():
            return Result.fail(f"{file_path} does not exist.")
        if not file.is_file():
            return Result.fail(f"{file_path} is not a regular file.")

        text = Path.read_text(file)
        count = text.count(old_string)

        if count == 0:
            return Result.fail(
                f"Could not find old_string in {file_path}. "
                "Copy the exact text from read_file, including spaces and indentation."
            )

        if count > 1 and not replace_all:
            return Result.fail(
                f"old_string appears {count} times in {file_path}. "
                "Either include more surrounding lines so it is unique, "
                "or pass replace_all=True to change every copy."
            )

        updated = text.replace(old_string, new_string, -1 if replace_all else 1)

        tmp_name = None
        try:
            fd, tmp_name = tempfile.mkstemp(dir=file.parent, prefix=f".{file.name}.", suffix=".tmp")

            with os.fdopen(fd, "w", encoding="utf-8", newline="") as fh:
                fh.write(updated)
                fh.flush()
                os.fsync(fh.fileno())

            shutil.copymode(file, tmp_name)
            os.replace(tmp_name, file)
        finally:
            if tmp_name is not None:
                Path(tmp_name).unlink(missing_ok=True)

        return Result.success(f"{file} edited successfully.")

    except PermissionError as e:
        return Result.fail(str(e))
    except FileNotFoundError:
        return Result.fail(f"{file_path} does not exist.")
    except Exception as e:
        return Result.fail(f"Error: Couldn't edit file. {e}")

def build_filesystem_tools(root: str) -> dict[str, Tool]:
    root = Path(root).resolve()
    return {
        "list_files": Tool(
            name="list_files",
            description="List files in an existing directory",
            func=partial(_list_files, root=root),
            arguments=[
                ("directory_path", "str")
            ]
        ),
        "read_file": Tool(
            name="read_file",
            description="Read the contents of a text file",
            func=partial(_read_file, root=root),
            arguments=[
                ("file_path", "str")
            ]
        ),
        "write_file": Tool(
            name="write_file",
            description="Write content to a new file. Fails if the file already exists",
            func=partial(_write_file, root=root),
            arguments=[
                ("file_path", "str"),
                ("content", "str")
            ]
        ),
        "delete_file": Tool(
            name="delete_file",
            description="Delete a file. Requires a reason for the deletion",
            func=partial(_delete_file, root=root),
            arguments=[
                ("file_path", "str"),
                ("reason", "str")
            ]
        ),
        "edit_file": Tool(
            name="edit_file",
            description="Edit a file. Append, Update, or Delete lines",
            func=partial(_edit_file, root=root),
            arguments=[
                ("file_path", "str"),
                ("old_string", "str"),
                ("new_string", "str"),
                ("replace_all", "bool")
            ]
        )
    }

FILESYSTEM_TOOLS = build_filesystem_tools(ROOT_PATH)
