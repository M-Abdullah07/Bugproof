# Issue tracker

Use GitHub Issues at https://github.com/M-Abdullah07/Bugproof/issues.
Git remote `origin` is https://github.com/M-Abdullah07/Bugproof.git; branch `main`.
Issues are enabled and authenticated write access was verified during setup.

Use `gh` if available. It is currently absent; GitHub REST authenticated through
Git Credential Manager is the verified fallback. Keep credentials in memory;
never place tokens in documents, command output or committed scripts.

"Publish a spec" means create or update a GitHub issue, checking for duplicates
first. The canonical BugProof spec is `docs/specs/bugproof.md`; its issue has not
been published. Automatic approval review rejected the attempted public issue
publication because explicit approval of that specific publication was missing.
Obtain that approval before retrying. The user separately authorized committing
and pushing local project files to origin main.

PRs as a request surface: **no**.
Labels are defined in `docs/agents/triage-labels.md`.
The implementation hold in AGENTS.md takes precedence over ticket status.
