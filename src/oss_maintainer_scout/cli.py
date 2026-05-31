from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from .report import render_json, render_markdown
from .scanner import RepositoryNotFoundError, scan_repository
from .scoring import score_scan


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="oss-scout",
        description="Scan a repository for open-source maintainer readiness.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="scan a local repository")
    scan_parser.add_argument("path", type=Path, help="path to the repository")
    scan_parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="output format",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "scan":
        try:
            scan = scan_repository(args.path)
        except RepositoryNotFoundError as exc:
            print(str(exc), file=sys.stderr)
            return 2

        score = score_scan(scan)
        if args.format == "json":
            print(render_json(scan, score), end="")
        else:
            print(render_markdown(scan, score), end="")
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2
