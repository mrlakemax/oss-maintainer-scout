from __future__ import annotations

import json
from dataclasses import asdict

from .models import ScanResult, ScoreResult


def render_markdown(scan: ScanResult, score: ScoreResult) -> str:
    lines = [
        "# OSS Maintainer Scout Report",
        "",
        f"Repository: `{scan.root}`",
        f"Score: {score.score}/100 ({score.earned_points}/{score.total_points} points)",
        f"Grade: {score.grade}",
        "",
        "## Passing Checks",
    ]

    passed_checks = [check for check in scan.checks if check.passed]
    if passed_checks:
        for check in passed_checks:
            found = ", ".join(f"`{path}`" for path in check.found_paths)
            lines.append(f"- {check.label}: found {found}")
    else:
        lines.append("- None yet")

    lines.extend(["", "## Missing High-Impact Items"])
    missing_required = [check for check in scan.checks if check.required and not check.passed]
    if missing_required:
        for check in missing_required:
            lines.append(f"- {check.label} - {check.recommendation}")
    else:
        lines.append("- None")

    optional_missing = [check for check in scan.checks if not check.required and not check.passed]
    lines.extend(["", "## Optional Improvements"])
    if optional_missing:
        for check in optional_missing:
            lines.append(f"- {check.label} - {check.recommendation}")
    else:
        lines.append("- None")

    lines.extend(["", "## Next Actions"])
    if score.recommendations:
        for index, recommendation in enumerate(score.recommendations, start=1):
            lines.append(f"{index}. {recommendation}")
    else:
        lines.append("1. Keep the project active with real issues, releases, and contributor feedback.")

    return "\n".join(lines) + "\n"


def render_json(scan: ScanResult, score: ScoreResult) -> str:
    payload = {
        "tool": "oss-maintainer-scout",
        "repository": str(scan.root),
        "score": asdict(score),
        "checks": {
            check.id: {
                "label": check.label,
                "category": check.category,
                "weight": check.weight,
                "required": check.required,
                "severity": check.severity,
                "passed": check.passed,
                "found_paths": list(check.found_paths),
                "recommendation": check.recommendation,
            }
            for check in scan.checks
        },
    }
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"
