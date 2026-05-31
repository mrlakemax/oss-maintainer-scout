from __future__ import annotations

from pathlib import Path

from .models import CHECK_DEFINITIONS, CheckDefinition, CheckResult, ScanResult


class RepositoryNotFoundError(ValueError):
    """Raised when the requested repository path cannot be scanned."""


IGNORED_DIRECTORIES = {
    ".git",
    ".hg",
    ".svn",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
}


def scan_repository(path: Path | str) -> ScanResult:
    root = Path(path).expanduser()
    if not root.exists() or not root.is_dir():
        raise RepositoryNotFoundError(f"Repository path does not exist: {root}")

    root = root.resolve()
    relative_paths = _collect_relative_paths(root)
    checks = tuple(_evaluate_check(definition, relative_paths) for definition in CHECK_DEFINITIONS)
    return ScanResult(root=root, checks=checks)


def _collect_relative_paths(root: Path) -> tuple[str, ...]:
    paths: list[str] = []
    for item in root.rglob("*"):
        if any(part in IGNORED_DIRECTORIES for part in item.relative_to(root).parts):
            continue
        if item.is_file():
            paths.append(item.relative_to(root).as_posix())
    return tuple(sorted(paths, key=str.lower))


def _evaluate_check(definition: CheckDefinition, relative_paths: tuple[str, ...]) -> CheckResult:
    matches = tuple(path for path in relative_paths if _matches(definition.id, path))
    return CheckResult(
        id=definition.id,
        label=definition.label,
        category=definition.category,
        weight=definition.weight,
        required=definition.required,
        severity=definition.severity,
        passed=bool(matches),
        found_paths=matches,
        recommendation=definition.recommendation,
    )


def _matches(check_id: str, relative_path: str) -> bool:
    lower_path = relative_path.lower()
    name = Path(lower_path).name

    if check_id == "readme":
        return name in {"readme", "readme.md", "readme.rst", "readme.txt"}
    if check_id == "license":
        return name in {"license", "license.md", "license.txt", "copying", "copying.md"}
    if check_id == "contributing":
        return name in {"contributing", "contributing.md", "contributing.rst"}
    if check_id == "code_of_conduct":
        return name in {
            "code_of_conduct",
            "code_of_conduct.md",
            "code-of-conduct",
            "code-of-conduct.md",
        }
    if check_id == "security":
        return name in {"security", "security.md"}
    if check_id == "issue_template":
        return lower_path.startswith(".github/issue_template") or lower_path.startswith(
            ".github/issue_template/"
        )
    if check_id == "pull_request_template":
        return name in {"pull_request_template.md", "pull-request-template.md"} or lower_path.startswith(
            ".github/pull_request_template/"
        )
    if check_id == "ci":
        return (
            lower_path.startswith(".github/workflows/")
            and lower_path.endswith((".yml", ".yaml"))
        ) or lower_path in {".gitlab-ci.yml", "azure-pipelines.yml", ".circleci/config.yml"}
    if check_id == "tests":
        return _is_test_path(lower_path, name)
    if check_id == "changelog":
        return name in {
            "changelog",
            "changelog.md",
            "changes.md",
            "history.md",
            "news.md",
            "release-notes.md",
            "release_notes.md",
        }
    return False


def _is_test_path(lower_path: str, name: str) -> bool:
    if lower_path.startswith(("tests/", "test/")):
        return True
    if name.startswith("test_") and name.endswith(".py"):
        return True
    return name.endswith((".test.ts", ".test.tsx", ".spec.ts", ".spec.tsx", ".test.js", ".spec.js"))
