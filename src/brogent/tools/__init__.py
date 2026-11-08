from .python_executor import execute_python
from .filesystem import file_operation

TOOLS = {
    "execute_python": execute_python,
    "file_operation": file_operation
}
