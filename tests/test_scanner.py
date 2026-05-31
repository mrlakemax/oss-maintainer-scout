from pathlib import Path

import pytest

from oss_maintainer_scout.scanner import RepositoryNotFoundError, scan_repository


def write_file(root: Path, relative_path: str, content: str = "content") -> None:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def checks_by_id(result):
    return {check.id: check for check in result.checks}


def test_scan_detects_core_community_and_automation_files(tmp_path):
    write_file(tmp_path, "README.md", "# Demo")
    write_file(tmp_path, "LICENSE", "MIT")
    write_file(tmp_path, "SECURITY.md", "# Security")
    write_file(tmp_path, "CHANGELOG.md", "# Changelog")
    write_file(tmp_path, ".github/workflows/ci.yml", "name: CI")
    write_file(tmp_path, ".github/ISSUE_TEMPLATE/bug_report.md", "bug")
    write_file(tmp_path, ".github/pull_request_template.md", "checklist")
    write_file(tmp_path, "tests/test_demo.py", "def test_demo(): assert True")

    result = scan_repository(tmp_path)
    checks = checks_by_id(result)

    assert checks["readme"].passed is True
    assert checks["license"].found_paths == ("LICENSE",)
    assert checks["security"].passed is True
    assert checks["changelog"].passed is True
    assert checks["ci"].found_paths == (".github/workflows/ci.yml",)
    assert checks["issue_template"].passed is True
    assert checks["pull_request_template"].passed is True
    assert checks["tests"].passed is True
    assert checks["contributing"].passed is False


def test_scan_matches_common_file_names_case_insensitively(tmp_path):
    write_file(tmp_path, "readme.MD", "# Demo")
    write_file(tmp_path, "license.txt", "MIT")
    write_file(tmp_path, "docs/CONTRIBUTING.md", "# Contributing")
    write_file(tmp_path, ".github/CODE_OF_CONDUCT.md", "# Conduct")

    checks = checks_by_id(scan_repository(tmp_path))

    assert checks["readme"].found_paths == ("readme.MD",)
    assert checks["license"].found_paths == ("license.txt",)
    assert checks["contributing"].found_paths == ("docs/CONTRIBUTING.md",)
    assert checks["code_of_conduct"].found_paths == (".github/CODE_OF_CONDUCT.md",)


def test_scan_rejects_missing_repository(tmp_path):
    with pytest.raises(RepositoryNotFoundError):
        scan_repository(tmp_path / "missing")
