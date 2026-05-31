from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CheckDefinition:
    id: str
    label: str
    category: str
    weight: int
    required: bool
    severity: str
    recommendation: str


@dataclass(frozen=True)
class CheckResult:
    id: str
    label: str
    category: str
    weight: int
    required: bool
    severity: str
    passed: bool
    found_paths: tuple[str, ...]
    recommendation: str


@dataclass(frozen=True)
class ScanResult:
    root: Path
    checks: tuple[CheckResult, ...]


@dataclass(frozen=True)
class ScoreResult:
    earned_points: int
    total_points: int
    score: int
    grade: str
    missing_required_ids: list[str]
    recommendations: list[str]


CHECK_DEFINITIONS: tuple[CheckDefinition, ...] = (
    CheckDefinition(
        id="readme",
        label="README",
        category="documentation",
        weight=12,
        required=True,
        severity="high",
        recommendation="Add a README that explains what the project does, who it is for, and how to run it.",
    ),
    CheckDefinition(
        id="license",
        label="LICENSE",
        category="legal",
        weight=14,
        required=True,
        severity="high",
        recommendation="Add a LICENSE file with an OSI-approved license such as MIT or Apache-2.0.",
    ),
    CheckDefinition(
        id="contributing",
        label="CONTRIBUTING",
        category="community",
        weight=9,
        required=True,
        severity="medium",
        recommendation="Add CONTRIBUTING.md with setup, testing, issue, and pull request guidance.",
    ),
    CheckDefinition(
        id="code_of_conduct",
        label="CODE_OF_CONDUCT",
        category="community",
        weight=7,
        required=False,
        severity="medium",
        recommendation="Add CODE_OF_CONDUCT.md so contributors know the collaboration norms.",
    ),
    CheckDefinition(
        id="security",
        label="SECURITY",
        category="security",
        weight=10,
        required=True,
        severity="high",
        recommendation="Add SECURITY.md with a private vulnerability reporting process.",
    ),
    CheckDefinition(
        id="issue_template",
        label="Issue template",
        category="maintenance",
        weight=7,
        required=False,
        severity="medium",
        recommendation="Add GitHub issue templates for bugs, features, and support questions.",
    ),
    CheckDefinition(
        id="pull_request_template",
        label="Pull request template",
        category="maintenance",
        weight=7,
        required=False,
        severity="medium",
        recommendation="Add a pull request template with test, documentation, and risk checkboxes.",
    ),
    CheckDefinition(
        id="ci",
        label="CI",
        category="automation",
        weight=12,
        required=True,
        severity="high",
        recommendation="Add CI that runs tests and quality checks on pull requests.",
    ),
    CheckDefinition(
        id="tests",
        label="Tests",
        category="quality",
        weight=12,
        required=True,
        severity="high",
        recommendation="Add tests that verify core behavior and can run in CI.",
    ),
    CheckDefinition(
        id="changelog",
        label="Changelog",
        category="release",
        weight=10,
        required=False,
        severity="low",
        recommendation="Add CHANGELOG.md or release notes so users can track changes.",
    ),
)
