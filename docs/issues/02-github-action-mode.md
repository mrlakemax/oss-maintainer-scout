# Add GitHub Action Mode

## Goal

Make `oss-maintainer-scout` easy to run in CI and pull requests.

## Proposed Behavior

Add a GitHub Action workflow example and an output mode suitable for GitHub Step Summary.

## Acceptance Criteria

- Adds documentation for running the scanner in GitHub Actions.
- Supports a CI-friendly output mode.
- Keeps the command deterministic and offline-first for local repositories.
- Includes tests for the new report output.
