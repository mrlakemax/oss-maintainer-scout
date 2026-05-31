from pathlib import Path

from oss_maintainer_scout.scanner import scan_repository
from oss_maintainer_scout.scoring import score_scan


def write_file(root: Path, relative_path: str, content: str = "content") -> None:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def create_complete_repo(root: Path) -> None:
    write_file(root, "README.md", "# Demo")
    write_file(root, "LICENSE", "MIT")
    write_file(root, "CONTRIBUTING.md", "# Contributing")
    write_file(root, "CODE_OF_CONDUCT.md", "# Conduct")
    write_file(root, "SECURITY.md", "# Security")
    write_file(root, "CHANGELOG.md", "# Changelog")
    write_file(root, ".github/workflows/ci.yml", "name: CI")
    write_file(root, ".github/ISSUE_TEMPLATE/bug_report.md", "bug")
    write_file(root, ".github/pull_request_template.md", "checklist")
    write_file(root, "tests/test_demo.py", "def test_demo(): assert True")


def test_complete_repository_gets_a_grade(tmp_path):
    create_complete_repo(tmp_path)

    score = score_scan(scan_repository(tmp_path))

    assert score.score == 100
    assert score.grade == "A"
    assert score.missing_required_ids == []
    assert score.recommendations == []


def test_sparse_repository_gets_actionable_recommendations(tmp_path):
    write_file(tmp_path, "README.md", "# Demo")

    score = score_scan(scan_repository(tmp_path))

    assert score.score < 60
    assert score.grade in {"D", "F"}
    assert "license" in score.missing_required_ids
    assert "ci" in score.missing_required_ids
    assert "tests" in score.missing_required_ids
    assert any("Add a LICENSE" in item for item in score.recommendations)
    assert any("Add CI" in item for item in score.recommendations)
