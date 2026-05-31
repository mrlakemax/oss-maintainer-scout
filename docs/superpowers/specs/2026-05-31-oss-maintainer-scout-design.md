# oss-maintainer-scout Design

## Goal

Build a real open-source maintainer utility that helps project owners evaluate whether a repository is ready for healthy public collaboration and maintainer automation.

The first release is a Python CLI that scans a local repository and produces an OSS readiness report. It should be useful without API keys, easy to test, and easy to extend later with GitHub and OpenAI-assisted issue, pull request, release, and security workflows.

## Users

- Open-source maintainers preparing a repository for public contributors.
- Solo developers who want a concrete checklist before publishing a project.
- Maintainers applying for maintainer-support programs who need honest evidence about repo maturity.

## Core Workflow

1. User runs `oss-scout scan /path/to/repo`.
2. The scanner checks for community and maintenance signals:
   - README
   - LICENSE
   - CONTRIBUTING
   - CODE_OF_CONDUCT
   - SECURITY
   - issue templates
   - pull request template
   - CI workflow
   - test files
   - changelog
   - release notes
3. The scorer assigns weighted points and severity levels.
4. The reporter prints either Markdown or JSON.
5. The report lists passing checks, missing checks, score, grade, and next actions.

## Architecture

The CLI is intentionally small and offline-first.

- `cli.py` parses arguments and writes output.
- `scanner.py` inspects repository files and returns normalized check results.
- `scoring.py` converts check results into score, grade, and recommendations.
- `report.py` renders Markdown and JSON.
- Tests use temporary repositories so behavior is deterministic.

The first version avoids network calls and LLM calls. That keeps the project safe to run in CI and makes it credible as a foundation for future maintainer automation.

## Future Roadmap

- GitHub URL scanning through the GitHub API.
- GitHub Action that comments on PRs with readiness changes.
- Optional OpenAI/Codex-powered issue triage and PR review checklists.
- Optional Codex Security summary for repositories with dependency manifests.
- Application-helper command that drafts evidence for maintainer-support forms from real repository metadata.

## Non-Goals

- It will not fabricate project popularity, adoption, or eligibility.
- It will not submit applications automatically.
- It will not require OpenAI API keys for the first release.
- It will not automate platform-specific publishing workflows.

## Success Criteria

- The repository has MIT license, README, contributing guide, security policy, changelog, code of conduct, tests, and CI.
- `python -m pytest` passes.
- `python -m oss_maintainer_scout scan . --format markdown` prints a useful report.
- `python -m oss_maintainer_scout scan . --format json` prints valid JSON.
- The README explains honest limits: a new project cannot guarantee acceptance into any external program, but strong maintainer workflows improve the case.
