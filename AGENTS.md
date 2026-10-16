# Agentika project

## Current scope

BugProof's MVP scope is approved. The user explicitly paused implementation:
documentation only until they directly resume development. No application code
or deployment exists. Organizer development permission is confirmed; retain fastn
MCP centrally while its event requirement remains unclear.

For specification, implementation planning, or acceptance review, read
`docs/specs/bugproof.md`. Use `GLOSSARY.md` for domain terms. The specification is
the implementation contract; earlier candidate/research documents are historical.
GitHub Issues is configured; the participant chose to leave the specification
unpublished as an issue. Keep it in the repository unless directly instructed otherwise.

## Local skills and tools

- Skills are project-local under `.agents/skills`; do not install globally.
- Before using gstack tools, dot-source `scripts/local-tools-env.ps1` in the
  same PowerShell command. Use Git for Windows Bash for its shell scripts.
- Use `scripts/setup-local-gstack.ps1` for setup; it keeps state and caches
  inside `.tools/` and redirects upstream's remaining home state writes.
- Keep telemetry and automatic upgrades off. Do not run upstream setup or an
  upgrade directly; inspect it for global writes first.
- Use one relevant skill at a time. Prefer concise planning and one complete
  workflow. Installed skills do not authorize external actions or subagents.
- No subagents unless the user explicitly requests delegation.
- Matt Pocock's skills use the project configuration below.
- Exclude `.vendor/` and tool dependencies from routine application searches.

## Agent skills

- For issue creation, updates or lookup, read `docs/agents/issue-tracker.md`.
- For triage, read `docs/agents/triage-labels.md` for the five configured labels.
- For domain modeling or architecture decisions, read `docs/agents/domain.md`.

## Event constraints supplied by participants

- Organizer development approval is confirmed. Conservatively retain fastn MCP
  and mandatory deployment on Alternate Clouds; implementation remains paused.
- The human decision must change what the automation may do.
- Submission cutoff: October 17, 2026, 12:45 PM Asia/Karachi. No code or
  deployment changes after cutoff; keep the deployment running until closing.
- Demo video: 2–3 minutes. Finalist presentation: exactly five minutes;
  finalist slide PDF due before 4 PM October 17.
- Participants must write LinkedIn/Twitter posts themselves; grammar help only.
- Keep credentials private. Use synthetic support reports and isolated test API
  records. Missing or conflicting customer facts require review; preserve uncertainty.
