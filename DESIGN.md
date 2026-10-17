# BugProof workspace design

The interface follows the operator's task: inspect source, gather evidence,
make a human decision, then verify delivery. Presentation stays in templates and
one shared stylesheet; approval, experiment and publication rules stay server-side.

## Visual system

- Ink `#192333`, muted text `#586477`, canvas `#f3f5f8`, borders `#dce2e9`.
- Navigation `#121b2b`; primary action blue `#244fe5`; human review amber `#946000`.
- System fonts; 14px panel radius; 24px grid gap; 44px minimum form/button targets.
- Green means verified completion, amber means review/information, red means error.
  Status is always named in text, so color carries no exclusive meaning.

## HCI choices

1. Recognition: four labeled workflow steps and section links keep the task visible.
2. Hierarchy: source and experiment sit together; large observed order count precedes
   trace details. Technical observations remain expandable to reduce reading load.
3. Human control: the review panel has a distinct amber boundary; save, reject,
   approve and publish retain separate actions and exact server validation.
4. Consistency: shared tokens, controls and spacing across login, inbox and case views.
5. Accessibility: skip link, semantic navigation/labels, visible keyboard focus,
   alert roles, reduced-motion support and a single-column narrow layout.

These are implemented design choices, not a claim of a formal accessibility audit
or measured usability improvement. See the UI evidence record for observed checks.
