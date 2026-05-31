import json
from pathlib import Path

from oss_maintainer_scout.report import render_json, render_markdown
from oss_maintainer_scout.scanner import scan_repository
from oss_maintainer_scout.scoring import score_scan


def write_file(root: Path, relative_path: str, content: str = "content") -> None:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_markdown_report_contains_score_sections_and_missing_items(tmp_path):
    write_file(tmp_path, "README.md", "# Demo")

    scan = scan_repository(tmp_path)
    score = score_scan(scan)
    markdown = render_markdown(scan, score)

    assert markdown.startswith("# OSS Maintainer Scout Report")
    assert "Score:" in markdown
    assert "## Missing High-Impact Items" in markdown
    assert "- LICENSE" in markdown
    assert "## Next Actions" in markdown


def test_json_report_is_parseable_and_stable(tmp_path):
    write_file(tmp_path, "README.md", "# Demo")
    write_file(tmp_path, "LICENSE", "MIT")

    payload = json.loads(render_json(scan_repository(tmp_path), score_scan(scan_repository(tmp_path))))

    assert payload["tool"] == "oss-maintainer-scout"
    assert payload["score"]["grade"] in {"A", "B", "C", "D", "F"}
    assert payload["checks"]["readme"]["passed"] is True
    assert payload["checks"]["license"]["found_paths"] == ["LICENSE"]
