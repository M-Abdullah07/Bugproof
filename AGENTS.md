# Agentika project

## Current scope

BugProof's MVP scope is approved. The user explicitly paused implementation:
documentation only until they directly resume development. No application code
or deployment exists. Organizer development permission is confirmed; retain fastn
MCP centrally while its event requirement remains unclear.

For exact behavior or scope changes, read `docs/specs/bugproof.md` (implementation
contract). Earlier candidate/research documents are historical.
GitHub Issues is configured; the participant chose to leave the specification
unpublished as an issue. Keep it in the repository unless directly instructed otherwise.

## Task navigation and evidence

- Before changing a decision or reopening a tradeoff, read `Decisions.md`.
- Before implementation planning or editing source boundaries, read `Architecture.md`.
  Its source/test paths are planned until code exists; create no placeholder modules during the hold.
- For milestone execution or a build handoff, read `docs/implementation-plan.md`;
  follow its dependencies and exit checks after explicit resume, recording actual evidence.
- Before tests, acceptance claims or verification work, read `ACCEPTANCE.md`.
  Update affected IDs with actual replay commands, commit/build identity and observed evidence;
  mark prior evidence stale after relevant changes. Never treat a provider double as live proof.
- Before demo, pitch or submission work, read `docs/judge_scorecard.md`.
- For domain terms, read `GLOSSARY.md`. For startup/run/test commands, use `README.md`
  and actual manifests; no application commands exist yet.
- Search first-party paths first: `rg --files docs scripts` and the named root documents.
  Once source exists, target `src/` and `tests/`; reach `.agents/skills` only for a selected skill.
- End each change with matching docs/evidence updates and a concise statement of
  what was verified versus what remains unknown. Keep module dependencies one-way.

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
