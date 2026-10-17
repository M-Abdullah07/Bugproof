# BugProof decisions

Execution: **RESUMED October 17, 2026** by direct participant instruction (DEC-16).
Behavioral contract: [specification](docs/specs/bugproof.md). This ledger records
decisions and reasons; it does not silently amend that contract. Direct human
instructions take precedence; record any changed decision and update affected docs.

## Binding decisions

| ID | Decision | Why it survives | Authority / provenance |
| --- | --- | --- | --- |
| DEC-01 | SUPERSEDED by DEC-16: previous documentation-only hold | Records the earlier instruction without treating it as current | Prior direct participant instruction |
| DEC-02 | Serve a support engineer: Gmail report to engineering handoff and reporter reply | One operator, one complete observable rescue | Participant chose support-to-engineering handoff |
| DEC-03 | Demonstrate duplicate orders after retry; replay corrected behavior and request missing information | Actual state distinguishes outcomes; avoids a canned success-only demo | Participant selected anchor incident and assembled MVP |
| DEC-04 | Auto-run bounded experiments against a registered isolated test API | Automates repetitive investigation without granting arbitrary execution | Participant approved bounded auto-run; specification defines limits |
| DEC-05 | Human may change expectation/disposition and must approve exact external actions | Judgment changes permitted effects; approval is enforced by the server | Participant approved assembled MVP and human control |
| DEC-06 | One FastAPI app, SQLite, server-rendered workspace, one structured-output LLM | Small stack; state and authority remain inspectable | Specification baseline; physical file layout remains flexible |
| DEC-07 | fastn MCP centrally connects Gmail and GitHub | Conservatively satisfies the unresolved framework rule and provides real integrations | Participant-supplied rules and approved MVP; no waiver confirmed |
| DEC-08 | SQLite durably claims each publication action before provider I/O | Prevents concurrent sends without adding a broker; timeout still requires reconciliation | Engineering review D2: participant chose recommended SQLite claim |
| DEC-09 | Main test seam is authenticated app API + actual lab HTTP + controlled model/provider responses; separate live smoke | Repeatable adverse cases plus independent proof of real connections | Participant explicitly approved testing boundary |
| DEC-10 | Deploy on Alternate Clouds; prove durable state before claiming restart recovery | Hosting eligibility and recovery are part of completion | Participant-supplied event constraints and specification |
| DEC-11 | Synthetic reports, owned accounts/repository, isolated records; no production or payment claims | Accessible, reproducible demonstration with honest limits | Approved MVP and specification |
| DEC-12 | Retain five responsibility boundaries plus isolated lab target; no mandatory microservices or file count | Keeps authority and recovery separate with modest complexity | Engineering review D1: participant chose original arrangement |
| DEC-13 | Cut Trello, automatic fixes, arbitrary code/browser execution, extra agents, dashboards and generic API onboarding | Each distracts from completing the selected handoff | Approved assembled scope; specification Out of Scope |
| DEC-14 | GitHub is the project tracker; keep the specification out of GitHub Issues | Repository documentation is sufficient; avoids unnecessary public issue publication | Participant explicitly chose Leave unpublished after approval-review rejection |
| DEC-15 | No delegated agents without direct user authorization; local-only skills/state | Maintains the participant's working constraints | AGENTS.md / direct instructions |
| DEC-16 | Resume implementation; stop and ask at material ambiguity; notify user when a new account is needed | Enables building while retaining user alignment and account control | October 17 direct instruction: "Let's start implementation using all the material and plans that we have" |
| DEC-17 | Skip local Docker installation/builds; retain the existing Dockerfile for remote packaging if hosting requires it | Saves workstation setup time without assuming Alternate Clouds supports a Python process directly | Participant asked to avoid Docker overhead; local Python already runs; remote build/deployment remains unverified |
| DEC-18 | Use the participant's existing Gemini API access instead of requiring a Groq signup | Avoids unnecessary account setup; verify available structured-output model and actual quota before live use | Participant reported a Gemini key; assistant accepted it as suitable |

## Unverified dependencies

| Gate | Needed proof | If unavailable |
| --- | --- | --- |
| fastn connector capabilities and accounts | Intake, issue create/read-back, same-thread reply, reconciliation behavior | Stop dependent work and explicitly revise; no fake integration |
| Alternate Clouds + storage | Participant reports account with $5 balance; actual deployment and storage survival unverified | Resolve hosting/storage before recovery claims |
| Model and controlled Gmail credentials | [Gemini model listing verified](docs/evidence/20261017-gemini-model-access.md); selected model available; generation/quota and fastn/Gmail setup unverified | Keep credentials outside Git; no full-workflow success claim yet |
| Event fastn rule | Organizer clarification | Retain fastn centrally pending clarification |

Demand and time savings remain unvalidated. A successful synthetic demo does not
resolve those questions. Organizer permission to develop is confirmed; DEC-01 is
the participant's former separate hold, now superseded by DEC-16.

## Update rule

Keep IDs stable. For a reversal, mark the old entry superseded, record the actual
human answer/reason and date, and link the replacement. Update specification,
architecture, acceptance and scorecard only where that decision affects them.
Plans, labels, model advice and successful tests do not grant implementation permission.
