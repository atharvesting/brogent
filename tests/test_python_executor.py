from brogent.tools.python_executor import execute_python

def test_successful_code_returns_success():
    res = execute_python(code="print('hello')")
    assert res["success"] is True
    assert res["stdout"] == "hello\n"
    assert res["exit_code"] == 0

def test_failing_code_returns_failure():
    res = execute_python(code="print(1 / 0)")
    assert res["success"] is False
    assert res["stdout"] == ""
    assert "ZeroDivisionError" in res["stderr"]
    assert res["exit_code"] != 0

def test_syntax_error_returns_failure():
    res = execute_python(code="print('Hello world!'")
    assert res["success"] is False
    assert res["stdout"] == ""
    assert "SyntaxError" in res["stderr"]
    assert res["exit_code"] != 0

def test_timeout_returns_failure():
    res = execute_python(code="import time; time.sleep(5)", timeout_seconds=1)
    assert res["success"] is False
    assert res["stdout"] == ""
    assert "timed out" in res["stderr"]
    assert res["exit_code"] == -1

def test_result_has_expected_shape():
    res = execute_python(code="print('Hello world!')")
    assert "success" in res
    assert "stdout" in res
    assert "stderr" in res
    assert "exit_code" in res
    assert isinstance(res["success"], bool)
    assert isinstance(res["stdout"], str)
    assert isinstance(res["stderr"], str)
    assert isinstance(res["exit_code"], int)
