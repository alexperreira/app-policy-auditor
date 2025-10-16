# Contributing

Thanks for helping make privacy auditing more accessible! This guide explains how to set up your dev environment, propose changes, and get them merged.

## Ground rules

- Be respectful. See our Code of Conduct.
- Prefer **small, focused** PRs.
- Write **clear commit messages** using Conventional Commits (e.g., `feat:`, `fix:`, `docs:`, `chore:` ).
- Add/update docs when behavior changes.

## Development Setup

1. Clone the repo and create a venv.
2. `pip install -r requirements.txt`
3. Run: `python auditor.py --seed examples/seed_targets.txt --out report`

## Branching & Workflow

- Create a feature branch: `git checkout -b feat/rule-tuning`
- Commit with Conventional Commits:
  - `feat(rules): add biometric detection patterns`
  - `fix(extract): fallback to readability when Trafilatura fails`
  - `docs: update README with new flags`
- Open a PR to `main`, fill in the template, and link any issues.

## Style

- Python: keep it readable; prefer small functions and clear names.
- Config: put rule changes in `rules/` and document rationale in PR.

## Tests (Lightweight for now)

- Manual run across 5-10 popular apps; attach snippets in PR.
- If you add heavy logic, include unit tests under `tests/` (pytest welcome).

## Adding/Editing Rules

- Edit `rules/risk_rules.yaml`.
- Keep **description** human-readable.
- Use **non-greedy**, case-insensitive regex.
- Provide examples in the PR.

## AI Providers

- The AI step is optional. If adding providers, make configurable via environment variabels and keep prompts short.

## Security & Privacy

- Never commit API keys or personal data.
- Use cached text only for auditing; avoid storing raw PII.
- See `SECURITY.md` for reporting vulnerabilities.
