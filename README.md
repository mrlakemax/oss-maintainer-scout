# oss-maintainer-scout

`oss-maintainer-scout` is a local-first CLI for maintainers who want an honest readiness report before publishing, growing, or applying for open-source maintainer support programs.

It scans a repository for common open-source health signals, then prints a practical report with score, grade, missing high-impact items, and next actions.

## What It Checks

- README
- LICENSE
- CONTRIBUTING
- CODE_OF_CONDUCT
- SECURITY
- GitHub issue templates
- Pull request template
- CI workflow
- Tests
- Changelog or release notes

## Install

From a local checkout:

```bash
python -m pip install -e ".[dev]"
```

After installation:

```bash
oss-scout scan .
oss-scout scan . --format json
```

Without installation:

```bash
python -m oss_maintainer_scout scan .
python -m oss_maintainer_scout scan . --format json
```

## Example

```text
# OSS Maintainer Scout Report

Repository: `/path/to/repo`
Score: 76/100 (76/100 points)
Grade: C

## Missing High-Impact Items
- LICENSE - Add a LICENSE file with an OSI-approved license such as MIT or Apache-2.0.
```

## Why This Exists

Maintainers are often judged by visible repository signals: documentation, licensing, issue triage, pull request workflow, release hygiene, tests, and security process. This tool turns those signals into a repeatable local report.

The project does not fabricate adoption or guarantee acceptance into any external program. A new repository still needs real users, releases, issues, and maintainer activity. The goal is to help maintainers build that evidence honestly.

## Roadmap

- GitHub URL scanning.
- GitHub Action that comments on pull requests.
- Optional OpenAI/Codex issue triage.
- Optional pull request review checklist generation.
- Optional application evidence drafting from real repository metadata.

## Development

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
python -m oss_maintainer_scout scan .
```

## License

MIT
