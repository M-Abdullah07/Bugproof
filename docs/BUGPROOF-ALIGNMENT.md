# BugProof alignment

Status: scope approved; implementation explicitly paused. No application code.
The implementation contract is `docs/specs/bugproof.md`.

## Confirmed

- Product direction: bounded bug-report verification and human-directed follow-up.
- First operator: support engineer handing a customer's API report to engineering.
- Source: Gmail. Engineering destination: GitHub. Reply destination: original email thread.
- Trello is cut because it duplicates the engineering queue without a demonstrated need.
- Bounded, pre-authorized checks on the registered test API run automatically.
  The runner enforces permitted operations, isolated fixtures, and execution limits.
- The support engineer interprets the evidence, may correct expected behavior,
  chooses the disposition, and approves exact external publication actions.
  The AI has no direct authority to publish or access arbitrary production targets.
- Anchor incident: duplicate orders after a failed request is retried with the
  same retry identifier. Inspect order records; make no real-payment claim.
- Replay against a corrected service version to verify that results follow
  observed behavior. Include an incomplete report requiring clarification.
- Scope ends at evidence-backed handoff and customer communication. Automatic
  code fixes and real payments are excluded.
- Organizer development approval is confirmed by the participant.
- fastn status is unclear; conservatively use fastn MCP as the core integration layer.
- Deployment must use Alternate Clouds. Target readiness: October 17, noon PKT;
  official code/deployment cutoff: 12:45 PM PKT.
- No directly accessible business partner or live customer workflow is available.
  Use transparently labeled synthetic reports and a controlled test API.

## Execution status

The participant approved the assembled scope and the main API-level testing seam,
then explicitly held implementation. Documentation synthesis only is authorized.
GitHub Issues and origin are configured for M-Abdullah07/Bugproof; specification
issue publication was explicitly declined by the participant; keep the spec in Git.
Provider/account and deployment feasibility checks remain future build gates.

## Evaluation discipline

Reliability (25) and usefulness (20) take priority over feature count. Human
judgment (15) must change the disposition or action, with a server-enforced
publication boundary. Automation depth (15) requires real execution, integration
read-back, and recoverable partial failures. Creativity (15) must be demonstrated
through the workflow, with no global uniqueness claims. UX/presentation (10)
requires a clear claim/evidence/decision view and a complete short demonstration.
