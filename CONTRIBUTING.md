# Contributing

Thanks for helping improve oss-maintainer-scout.

## Local Setup

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -e ".[dev]"
python -m pytest -q
```

On macOS or Linux, activate with `source .venv/bin/activate`.

## Pull Requests

Before opening a pull request:

1. Add or update tests for behavior changes.
2. Run `python -m pytest -q`.
3. Update `README.md` or `CHANGELOG.md` when user-visible behavior changes.
4. Keep pull requests focused on one problem.

## Maintainer Workflow

This project favors small, reviewable changes. New checks should include:

- a scanner test for detection,
- a scoring or report test when output changes,
- documentation showing why the check matters to maintainers.
