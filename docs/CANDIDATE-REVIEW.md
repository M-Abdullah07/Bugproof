# Candidate review: BugProof

Status: BugProof selected by the participant; detailed workflow alignment in
progress. Not implemented. The earlier proposal below is being challenged and
may be revised before the final design is approved.
Reviewed October 16, 2026, Asia/Karachi. Target submission readiness: noon Oct 17.

## Confirmed alignment

- The participant currently has no directly accessible business workflow.
- Organizer permission to develop is confirmed by the participant in this chat.
- fastn requirements remain unclear. Conservatively make fastn MCP central and
  retain Alternate Clouds deployment; do not assume a waiver.
- The objective is one complete, reliable, consequential automation workflow.
- Previous domain ideas do not have validated customer adoption. Do not treat
  their research or demonstrations as proof of demand.

## Recommendation for discussion

BugProof turns a natural-language bug report into an inspectable, bounded API
reproduction, then lets a human decide and authorize the exact follow-up.
Working pitch: "AI checks what happened. A human decides what it means."

Target operator: a developer triaging reports for a small HTTP API. The proposed
first user segment has not been interviewed; public maintainer accounts establish
a workload problem, not demand for this particular implementation.

## Public evidence and disconfirmation

GitHub describes incoming contribution volume outpacing review capacity and has
introduced controls such as contributor PR limits.
[GitHub, June 2026](https://github.blog/open-source/maintainers/how-pull-request-limits-are-cutting-down-the-noise/).

curl's maintainer reports that, from March 2026, security submissions became
higher quality but remained an overload problem. This contradicts an overly
simple thesis that the whole problem is low-quality AI text. Our narrower
interpretation: verifying and acting on reports costs human attention even when
the reports are good. We do not claim our functional API demo solves curl's
security workload.
[Maintainer account, April 2026](https://daniel.haxx.se/blog/2026/04/22/high-quality-chaos/).

Existing GitHub automation supports issue triage and approvals; a new labeling
dashboard is insufficient differentiation.
[GitHub documentation](https://docs.github.com/en/copilot/concepts/agent-capabilities/agent-powered-workflows-and-operations/about-automation-rationale-and-approvals).

Bug reproduction is also an existing research/project category. One public
repository describes an autonomous reproducer, but its browsed tree is primarily
design documentation; its README alone does not establish production readiness.
[Public project](https://github.com/DanieleSuppo/autonomous-bug-reproducer),
[research paper](https://arxiv.org/abs/2502.01821).
No global novelty claim is justified. A distinctive hackathon execution would
combine bounded executable evidence, editable human interpretation, an enforced
action gate, and verified cross-system follow-through.

## Adversarial passes and resulting scope

| Pass | Strong objection | Refinement / consequence |
| --- | --- | --- |
| Need | Another AI summary adds material to review. | The output must include actual request/response evidence and the claimed-vs-observed result. |
| Novelty | Triage bots and repro agents already exist. | Do not market labeling or reproduction as inventions; show the complete evidence-to-action workflow. |
| Truth | Reproduced behavior does not prove a bug, and failure to reproduce does not disprove one. | Separate observed result from maintainer disposition; preserve inconclusive outcomes. |
| Human role | An approve button may become a rubber stamp. | Human confirms or edits expected behavior and can accept the bug, request evidence, or record intended behavior. |
| Scope | Universal repository checkout and arbitrary test execution will exceed the deadline. | One explicitly supported API contract and one trusted, resettable test service; no arbitrary repositories or generated shell execution. |
| Reliability | A report could instruct the agent to run commands or post externally. | Treat it as data; model emits a typed plan; fixed runner and server-side action endpoint enforce the allowed surface. |
| Integration | A successful local run followed by a task card is only a partial workflow. | Publish the approved disposition/evidence to the owned GitHub issue, create the appropriate engineering task only when needed, and read back both results. |
| Validity | The demo may be hardcoded to its example reports. | Run real API requests, store traces, accept paraphrases and changed input values, and show a non-reproduced case. |
| Adoption | A maintainer must still configure and inspect it. | Require one small API contract; expose the setup cost. Do not claim zero setup or proven time savings. |

These are sequential critiques from the same assistant, not independent reviews
or an empirical validation study. No subagents were used.

## Complete candidate workflow

1. Read a report from the team's own GitHub demonstration repository through fastn.
2. Extract the claimed behavior, supporting text, missing information, and a
   proposed request sequence against the supported API schema.
3. If inputs are missing, prepare a specific clarification request; do not invent
   data and call the report disproved. Otherwise the maintainer reviews the
   expected behavior and approves the bounded reproduction plan.
4. Execute allowed HTTP operations only on the registered test service. Capture
   actual requests, responses, state observations, fixture ID, and service version.
5. Show the trace beside the report. The maintainer chooses confirmed bug,
   more evidence needed, or intended behavior, with an editable explanation.
6. Show the exact GitHub comment/labels and optional Trello task for authorization.
   Server verifies the approved plan and current report version before writing.
7. Apply the selected actions through fastn, read them back, and expose links.
   Partial failures remain pending and retry only unfinished actions using stable IDs.

Completion is an accurately dispositioned report with inspectable evidence and
the authorized follow-up recorded. It is not a repaired or deployed product fix.

## Demonstration boundary

One trusted JSON API representing a tiny checkout/discount service, hosted with
the main application on Alternate Clouds. Use synthetic state and resettable
per-run fixtures. Example claim: the same single-use discount is accepted twice.
The observed trace must actually demonstrate repeated acceptance; an LLM verdict
alone cannot establish it. A second report lacks a required condition. A third
describes behavior that does not reproduce under its stated conditions.

The target is deliberately a laboratory service. Label it as such; do not imply
that the prototype autonomously reproduced a real vulnerability in curl or any
unaffiliated project. No security reports are sent to real maintainers.

## Three implementation approaches

| Approach | Effort | Risk | Trade-off |
| --- | --- | --- | --- |
| A: Evidence checklist only | Small | Low | Fastest, but little proof beyond summaries; reject as the final differentiator. |
| B: Bounded API replay + approved follow-through | Medium | Medium | Recommended: observable execution and complete automation with a constrained surface. |
| C: Arbitrary repo/browser reproduction and fixing | Extra large | High | Broader long-term coverage, but reject for tomorrow's deadline. |

The participant selected the bounded BugProof direction. A complete design
document will follow the current workflow alignment; this file remains research
and the original candidate decision brief.

## First execution gates after selection

- Confirm fastn can read/update an owned test GitHub issue and create/read an
  owned Trello card. The public connector catalog does not prove these actions
  work for our account. Do not spend hours on a dashboard before this passes.
- Deploy a health-checked shell to Alternate Clouds and verify PORT configuration.
- Implement one complete report-to-disposition path before adding more fixtures.
- Use server-owned provider credentials, validated tool arguments, persisted
  workflow state, and idempotent external writes. Never expose credentials to
  report content or generated prompts.
- Verify missing data, rejected human proposals, stale approvals, integration
  failure/retry, and a restarted worker preserving its completed actions.
- Reserve the morning for live rehearsal, video, screenshots, participant-written
  LinkedIn content, submission PDF, and presentation PDF. Target noon readiness;
  official code/deployment freeze remains Oct 17 at 12:45 PM PKT.

## Remaining decision

The first unresolved refinement is the operator: support-to-engineering handoff
(Gmail and GitHub), or developer triage originating in GitHub. Trello is challenged
as potentially redundant when GitHub already holds the engineering queue.
No business partner is required for a transparent lab demonstration, but external
integration accounts and a deployed test service are still required.
