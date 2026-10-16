# BugProof

A support report becomes evidence a developer can act on, followed by a
human-approved engineering handoff and reporter reply.

**Documentation only. Implementation is paused.** No application, test suite,
deployment or application startup command exists. The registered test API and
all demonstration reports will be synthetic and explicitly labeled.

## Start here

| Task | Read |
| --- | --- |
| Agent instructions and permissions | [AGENTS.md](AGENTS.md) |
| Exact behavior and scope | [Specification](docs/specs/bugproof.md) |
| Decisions and reasons | [Decisions.md](Decisions.md) |
| Ownership, dependencies and planned source map | [Architecture.md](Architecture.md) |
| Acceptance claims, run status and evidence | [ACCEPTANCE.md](ACCEPTANCE.md) |
| Competition proof and submission | [Judge scorecard](docs/judge_scorecard.md) |
| Domain vocabulary | [GLOSSARY.md](GLOSSARY.md) |

Older candidate/research/design documents preserve context; they do not override
the specification or later explicit participant decisions.

## Repository and tools

GitHub: https://github.com/M-Abdullah07/Bugproof, branch `main`.
The tracker is configured; the participant chose no public specification issue.
Development skills are project-local; tool state/caches are ignored. Gstack
source is a pinned submodule: clone with `--recurse-submodules`, or run
`git submodule update --init .agents/skills/gstack` in an existing clone.
Tool readiness and limitations: [local status](docs/LOCAL-TOOLS-STATUS.md).
Use `scripts/setup-local-gstack.ps1` for its project-local setup; never assume
tool installation means the product is implemented.

After implementation resumes, add verified install/run/test commands here as
soon as a runnable slice exists. Keep commands aligned with actual manifests;
use ACCEPTANCE.md to record what they proved. See [third-party licenses](docs/licenses/).
