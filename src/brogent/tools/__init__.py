from .python_executor import execute_python
from .filesystem import read_file, write_file, delete_file, edit_file, list_files

TOOLS = {
    "execute_python": execute_python,
    "list_files": list_files,
    "read_file": read_file,
    "write_file": write_file,
    "delete_file": delete_file,
    "edit_file": edit_file
}

TOOL_LIST = list(TOOLS.values())
