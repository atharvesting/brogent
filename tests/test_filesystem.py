from pathlib import Path
import pytest
from brogent.tools.filesystem import build_filesystem_tools


@pytest.fixture
def tools(tmp_path) -> dict:
    return build_filesystem_tools(tmp_path)


def test_write_file_creates_file(tools: dict, tmp_path: Path):
    full_path = tmp_path / "test.txt"
    expected = "hello"
    res = tools["write_file"](file_path=full_path, content=expected)
    assert res["success"] is True
    with open(full_path, "r") as f:
        s = f.read()
    assert s == expected


def test_read_file_accurate(tools: dict, tmp_path: Path):
    full_path = tmp_path / "test.txt"
    expected = "2 + 5 = 3___4"
    with open(full_path, "w") as f:
        f.write(expected)
    res = tools["read_file"](file_path=full_path)
    assert res["success"] is True
    assert res["stdout"] == expected


def test_delete_file_on_non_existent_file(tools: dict, tmp_path: Path):
    full_path = tmp_path / "test.txt"
    res = tools["delete_file"](file_path=full_path, reason="Test")
    assert res["success"] is False
    assert "Couldn't delete" in res["stderr"]


def test_delete_file_on_valid_file(tools: dict, tmp_path: Path):
    full_path = tmp_path / "test.txt"
    with open(full_path, "w") as f:
        f.write("Hi there!")

    res = tools["delete_file"](file_path=full_path, reason="Test")
    assert res["success"] is True
    assert "successfully deleted" in res["stdout"]
    assert not full_path.exists()


def test_edit_file_with_non_existent_string_returns_failure(tools: dict, tmp_path: Path):
    full_path = tmp_path / "test.txt"
    expected = "This is a test where edit_file receives a non-existent string"
    with open(full_path, "w") as f:
        f.write(expected)
    res = tools["edit_file"](file_path=full_path, old_string="brogent", new_string="bro + agent", replace_all=False)
    assert res["success"] is False
    assert "not find old_string" in res["stderr"]
    assert full_path.read_text(encoding="utf-8") == expected


def test_edit_file_with_valid_arguments_returns_success(tools: dict, tmp_path: Path):
    full_path = tmp_path / "test.txt"
    original = "def add(a, b):\n    return a - b\n"
    expected = "def add(a, b):\n    return a + b\n"
    full_path.write_text(original, encoding="utf-8")

    res = tools["edit_file"](
        file_path=full_path,
        old_string="return a - b",
        new_string="return a + b",
        replace_all=False,
    )

    assert res["success"] is True
    assert "edited successfully" in res["stdout"]
    assert full_path.read_text(encoding="utf-8") == expected


def test_edit_file_with_multiple_instances_without_replace_all_returns_failure(tools: dict, tmp_path: Path):
    full_path = tmp_path / "test.txt"
    original = "banana\n"
    full_path.write_text(original, encoding="utf-8")

    res = tools["edit_file"](
        file_path=full_path,
        old_string="a",
        new_string="o",
        replace_all=False,
    )

    assert res["success"] is False
    assert "appears 3 times" in res["stderr"]
    assert "replace_all=True" in res["stderr"]
    assert full_path.read_text(encoding="utf-8") == original


@pytest.mark.parametrize(
    ("overrides", "expected_field"),
    [
        ({"file_path": 123}, "file_path"),
        ({"old_string": 123}, "old_string"),
        ({"new_string": None}, "new_string"),
        ({"replace_all": "true"}, "replace_all"),
    ],
)
def test_edit_file_with_invalid_arg_types_returns_failure(
    tools: dict, tmp_path: Path, overrides: dict, expected_field: str
):
    full_path = tmp_path / "test.txt"
    original = "hello\n"
    full_path.write_text(original, encoding="utf-8")

    kwargs = {
        "file_path": full_path,
        "old_string": "hello",
        "new_string": "world",
        "replace_all": False,
    }
    kwargs.update(overrides)

    res = tools["edit_file"](**kwargs)

    assert res["success"] is False
    assert expected_field in res["stderr"]
    assert full_path.read_text(encoding="utf-8") == original


def test_edit_file_with_directory_path_returns_failure(tools: dict, tmp_path: Path):
    directory = tmp_path / "folder"
    directory.mkdir()

    res = tools["edit_file"](
        file_path=directory,
        old_string="a",
        new_string="b",
        replace_all=False,
    )

    assert res["success"] is False
    assert "not a regular file" in res["stderr"]


def test_edit_file_with_multiple_instances_replaces_all_successfully(tools: dict, tmp_path: Path):
    full_path = tmp_path / "test.txt"
    full_path.write_text("banana\n", encoding="utf-8")

    res = tools["edit_file"](
        file_path=full_path,
        old_string="a",
        new_string="o",
        replace_all=True,
    )

    assert res["success"] is True
    assert full_path.read_text(encoding="utf-8") == "bonono\n"


def test_list_files_with_file_path_returns_failure(tools: dict, tmp_path: Path):
    full_path = tmp_path / "test.txt"
    full_path.write_text("hello", encoding="utf-8")

    res = tools["list_files"](directory_path=full_path)

    assert res["success"] is False
    assert "points to a file path" in res["stderr"]


def test_list_files_with_valid_directory_path_returns_success(tools: dict, tmp_path: Path):
    (tmp_path / "a.txt").write_text("a", encoding="utf-8")
    (tmp_path / "b.txt").write_text("b", encoding="utf-8")
    (tmp_path / "nested").mkdir()

    res = tools["list_files"](directory_path=tmp_path)

    assert res["success"] is True
    lines = res["stdout"].splitlines()
    assert lines[0].startswith("Files inside")
    assert set(lines[1:]) == {"a.txt", "b.txt"}


def test_list_files_with_non_existent_directory_path_returns_failure(tools: dict, tmp_path: Path):
    res = tools["list_files"](directory_path=tmp_path / "missing")

    assert res["success"] is False
    assert "List operation failed" in res["stderr"]
