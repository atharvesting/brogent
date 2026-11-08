from subprocess import CompletedProcess

def subprocess_output(result: CompletedProcess):
    return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode
        }

def subprocess_output_specific(
        success: bool,
        stdout: str,
        stderr: str,
        exit_code: int
):
    return {
            "success": success == 0,
            "stdout": stdout,
            "stderr": stderr,
            "exit_code": exit_code
        }
