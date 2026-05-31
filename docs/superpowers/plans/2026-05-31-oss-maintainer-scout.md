# oss-maintainer-scout Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a tested Python CLI that scans local repositories and reports OSS maintainer-readiness.

**Architecture:** Keep scanning, scoring, rendering, and CLI concerns separate. Use deterministic local filesystem checks first, with a clean path for future GitHub/OpenAI integrations.

**Tech Stack:** Python 3.11+, argparse, dataclasses, pytest, GitHub Actions, MIT license.

---

## File Map

- `pyproject.toml`: package metadata, console script, pytest configuration.
- `README.md`: public-facing project explanation, install, usage, honest application guidance.
- `LICENSE`: MIT license.
- `CHANGELOG.md`: release history.
- `CONTRIBUTING.md`: contribution workflow.
- `CODE_OF_CONDUCT.md`: contributor behavior baseline.
- `SECURITY.md`: vulnerability reporting policy.
- `.github/workflows/ci.yml`: test workflow.
- `src/oss_maintainer_scout/models.py`: dataclasses and constants.
- `src/oss_maintainer_scout/scanner.py`: local repository inspection.
- `src/oss_maintainer_scout/scoring.py`: score, grade, and recommendations.
- `src/oss_maintainer_scout/report.py`: Markdown and JSON rendering.
- `src/oss_maintainer_scout/cli.py`: command-line interface.
- `src/oss_maintainer_scout/__main__.py`: `python -m` entry point.
- `tests/test_scanner.py`: scanner behavior.
- `tests/test_scoring.py`: scoring behavior.
- `tests/test_report.py`: output behavior.
- `tests/test_cli.py`: CLI behavior.

## Task 1: Project Skeleton

- [ ] Create package directories under `src/oss_maintainer_scout` and `tests`.
- [ ] Add `pyproject.toml` with package metadata and `oss-scout = "oss_maintainer_scout.cli:main"`.
- [ ] Add OSS community files: `LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CHANGELOG.md`.
- [ ] Add CI workflow that installs the package and runs `python -m pytest`.

## Task 2: Scanner TDD

- [ ] Write tests that create temporary repositories and assert detected/missing checks.
- [ ] Run `python -m pytest tests/test_scanner.py -q` and confirm failure because implementation does not exist yet.
- [ ] Implement `scan_repository(path: Path) -> ScanResult` with case-insensitive file matching for common OSS files.
- [ ] Re-run scanner tests until they pass.

## Task 3: Scoring TDD

- [ ] Write tests that assert complete repositories get high scores and missing license/security/CI reduce the score.
- [ ] Run `python -m pytest tests/test_scoring.py -q` and confirm failure before implementation.
- [ ] Implement weighted scoring, grade mapping, and recommendation generation.
- [ ] Re-run scoring tests until they pass.

## Task 4: Report TDD

- [ ] Write tests for Markdown headings, missing-item bullets, and JSON parseability.
- [ ] Run `python -m pytest tests/test_report.py -q` and confirm failure before implementation.
- [ ] Implement `render_markdown` and `render_json`.
- [ ] Re-run report tests until they pass.

## Task 5: CLI TDD

- [ ] Write tests for `scan`, `--format markdown`, `--format json`, and invalid path handling.
- [ ] Run `python -m pytest tests/test_cli.py -q` and confirm failure before implementation.
- [ ] Implement argparse CLI and module entry point.
- [ ] Re-run CLI tests until they pass.

## Task 6: Documentation And Verification

- [ ] Write README with install, usage, sample output, roadmap, and honest Codex for OSS application guidance.
- [ ] Run `python -m pytest -q`.
- [ ] Run `python -m oss_maintainer_scout scan . --format markdown`.
- [ ] Run `python -m oss_maintainer_scout scan . --format json`.
- [ ] Commit the completed project.
