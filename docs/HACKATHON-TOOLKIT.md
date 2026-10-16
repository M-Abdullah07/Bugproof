# Agentika toolkit

Prepared October 16, 2026. Project idea and organizer approval remain unresolved.

## Installed locally

- Official [gstack](https://github.com/garrytan/gstack), source commit
  `47d639abffa882b8cbb641d7d1dedf08ecada9ec`, in `.agents/skills/gstack`.
  Codex support is experimental upstream. Runtime build status is recorded
  separately in `LOCAL-TOOLS-STATUS.md`.
  Compiled helpers are blocked by this machine's Windows Application Control;
  installed instruction skills must not be confused with full runtime readiness.
- [Matt Pocock's skills](https://github.com/mattpocock/skills): 31 published
  engineering, productivity, and misc skills under `.agents/skills`.
  The local source snapshot is `49dd158d1076134a641b33efb035946536778336`.
  Installation used the official Codex skill installer against `main`.
  Its `in-progress` collection was excluded. The interactive setup wizard was
  not run. Claude-specific misc skills are present but irrelevant to Codex.
- Bun 1.4.3 is project-local in `.tools/bun`; no global PATH installation.
- All intended runtime state and download caches are under `.tools/`.
  Gstack telemetry, proactive invocation, and update checks are disabled.

Codex discovers project skills from `.agents/skills`; see the
[official skills documentation](https://learn.chatgpt.com/docs/build-skills).
They should become available on the next turn; reopen this project chat if the
skill list has not refreshed.

## Highest-yield skills

| Need | Use | Stop when |
| --- | --- | --- |
| Narrow the candidate | Matt's `grill-with-docs` OR gstack `office-hours` | One user, one rescue, one measurable outcome |
| Define the build | Matt's `to-spec`, then gstack `plan-eng-review` | Data contract, human gate, integrations, acceptance criteria fit on a page |
| Build reliably | Matt's `tdd` where failure matters | Approval, duplicate prevention, and retry behavior are covered |
| Find a blocker | Matt's `diagnosing-bugs` OR gstack `investigate` | Root cause is reproduced and fixed |
| Check the demo | gstack `qa-only`, then targeted fixes | The complete deployed rescue succeeds |
| Finish artifacts | Existing PDF/presentation skills | Submission PDF and five-minute deck are verified |

Do not run every planning skill in sequence. Avoid broad refactors, architecture
audits, multiple agent frameworks, and automatic release/deploy workflows during
the hackathon. Existing spreadsheet/PDF/presentation skills are already available;
there is no need to install duplicates.

## Recommended integrations and tools, in order

1. **fastn MCP for application integrations.** Resolve the rule discrepancy
   with organizers. If this direction is accepted, use fastn for Google Sheets
   intake and Trello counselor tasks, making its role visible in the demo.
   Official sources: [MCP server](https://github.com/fastn-ai/fastn-mcp),
   [Sheets connector](https://fastn.ai/integrations/google-sheets), and
   [Trello connector](https://fastn.ai/integrations/trello).
   Hosted OAuth and tool availability must be checked with your account;
   a catalog listing is not proof that our connections work.
2. **GitHub CLI or connector for development.** Source control, review,
   deployment source, and submission repository. Prefer the CLI for routine
   local work if already authenticated. No account connection was made here.
3. **One browser QA tool.** Use the available browser capability first.
   Gstack's Chromium bootstrap is deferred. Add
   [Playwright MCP](https://github.com/microsoft/playwright-mcp) only if a
   browser capability gap appears; avoid duplicate browser toolsets.
4. **Sheets + Trello as the two live demo systems.** Desktop Google Drive
   and Trello plugins can help us inspect sample records/boards, but a desktop
   plugin connection does not wire the deployed app. The app needs its own
   configured integration access. Suggested plugins were not installed or
   connected, and would be account-level choices, separate from local skills.
5. **Alternate Clouds deployment and logs.** Treat this as mandatory.
   No verified provider-specific MCP configuration is available in this setup.
   Follow the supplied event guide: match PORT, set secrets, Rebuild → Deploy,
   verify health, and capture deployment evidence early.

Defer Ragic, Excel sync, SOP writing, and university portals for the hackathon.
If needed commercially, use the official Ragic API and supported Excel/Graph
access after confirming the actual data structure and hosting.

## Suggested candidate demo

Synthetic student application due soon → Sheets record conflicts and missing
document detected → evidence and proposed counselor tasks shown → counselor
corrects facts and approves the exact action → Trello tasks created and Sheets
status updated → visible readiness result and audit trail.

Use deterministic validation for required fields and dates. Use AI for grounded
explanation and proposed next actions. Bind approval to the exact case/version
and proposed writes. Use stable student IDs and idempotency keys so retrying
does not duplicate tasks. Revalidate if data changes after approval.

The most useful supporting artifacts are a resettable synthetic case, one
complete live run, a safe retry demonstration, visible before/after state, and
an integration failure that leaves the case recoverable. Deploy early, then
prepare the 2–3 minute video and exact five-minute presentation.

No application, credentials, deployment, posts, or external messages were
created by this tooling task.
