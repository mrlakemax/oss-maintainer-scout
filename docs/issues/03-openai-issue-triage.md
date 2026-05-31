# Add Optional OpenAI-Assisted Issue Triage

## Goal

Add an optional maintainer workflow that helps classify issues and draft next actions.

## Proposed Behavior

Use an OpenAI API key only when explicitly configured. The base scanner must remain usable without API keys.

## Acceptance Criteria

- API integration is optional and disabled by default.
- No issue data is sent externally unless the user opts in.
- Output includes issue category, missing reproduction details, suggested labels, and reply draft.
- Tests cover prompt-building and redaction behavior without making live API calls.
