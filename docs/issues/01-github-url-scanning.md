# Add GitHub URL Scanning

## Goal

Allow users to scan a public GitHub repository URL in addition to a local path.

## Proposed Behavior

```bash
oss-scout scan https://github.com/owner/repo
```

The command should fetch repository metadata and community files, then produce the same Markdown/JSON readiness report.

## Acceptance Criteria

- Supports public GitHub repository URLs.
- Keeps local scanning available without network access.
- Adds tests for URL parsing and metadata normalization.
- Documents GitHub API rate-limit behavior.
