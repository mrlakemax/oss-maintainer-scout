import json
from pathlib import Path

from oss_maintainer_scout.cli import main


def write_file(root: Path, relative_path: str, content: str = "content") -> None:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_cli_scan_outputs_markdown_by_default(tmp_path, capsys):
    write_file(tmp_path, "README.md", "# Demo")

    exit_code = main(["scan", str(tmp_path)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "# OSS Maintainer Scout Report" in captured.out
    assert captured.err == ""


def test_cli_scan_outputs_json(tmp_path, capsys):
    write_file(tmp_path, "README.md", "# Demo")
    write_file(tmp_path, "LICENSE", "MIT")

    exit_code = main(["scan", str(tmp_path), "--format", "json"])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert json.loads(captured.out)["checks"]["license"]["passed"] is True


def test_cli_returns_error_for_missing_path(tmp_path, capsys):
    exit_code = main(["scan", str(tmp_path / "missing")])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "Repository path does not exist" in captured.err
