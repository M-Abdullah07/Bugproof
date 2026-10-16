# Research: complete, consequential workflows for Agentika

Research date: October 16, 2026, Asia/Karachi. Target ready-to-submit time:
October 17, noon PKT. No idea is selected and organizer approval is unconfirmed.

Admissions in its current form, event recovery, customer promise rescue, and
handoff detective have been rejected by the participant. Earlier toolkit notes
are historical, not an accepted product brief.

## Method and boundaries

Research followed three passes: evidence of the problem; the causal mechanism
and existing solutions; a bounded workflow with observable execution and failure
handling. Sources below are regulators, government incident reports, and vendors'
own product documentation. Vendor research describes its observed sample, not
necessarily the entire population. No 2027 outcome is treated as an observed fact.
Relevance to 2027 is a planning inference, not a forecast established by evidence.

Research was conducted directly because the project's AGENTS.md prohibits
delegation without explicit user authorization. No account connections, external
messages, implementation, or deployment were performed.

The recommendation is a design judgment. No customer demand, willingness to pay,
connector account access, or deployment feasibility has been validated firsthand.
Novelty means a differentiated demonstration and intervention, not an assertion
that no competing product exists.

## Main finding

A strong recurring failure is that an upstream fact changes while downstream
decisions remain executable. More alerts do not repair that dependency. A useful
intervention identifies what depended on the old fact, holds affected operations,
gets a human decision grounded in evidence, applies the decision, and reads back
the resulting state. This is our synthesis, not a statistic claimed by a source.

For tomorrow, constrain the system to one organization, one change type, two live
integrations, one authority boundary, and one recovery path. Every proposed system
below has a boundary: a controlled dispatch workflow, a payment export, or a
reseller's own listing flow. It cannot enforce behavior outside that boundary.

## 1. Ingredient-change control — recommended new direction

### Evidence

FSA guidance requires appropriate checks when ingredient suppliers change and
describes maintaining awareness of supplier ingredient changes.
[Government guidance](https://www.gov.uk/government/publications/precautionary-allergen-labelling/precautionary-allergen-labelling).

An FSA consultation records that frequent menu/supplier changes make written
allergen information difficult to maintain, and identifies substitutions and
varying supplier information as challenges, especially for SMEs.
[Consultation findings](https://www.food.gov.uk/business-guidance/summary-of-stakeholder-responses-consultation-on-best-practice-guidance-allergen-information-for-non-prepacked-foods).

FSA research also places written communication within a wider operational system;
materials alone are insufficient, and some businesses struggled to adapt menus
for the study. This is research evidence, not a measured prevalence estimate for
Pakistan or a demonstration that our product would reduce injuries.
[FSA research, executive summary, pp. 5–7](https://science.food.gov.uk/api/v1/articles/123212-improving-allergen-communication-in-sme-food-businesses-in-out-of-home-settings.pdf).

### Causal mechanism and proposed user

For a small meal-prep kitchen or campus caterer, a delivery replaces the usual
sauce with another brand. The kitchen recognizes the same functional ingredient,
but its allergen information may differ. Recipes, customer-facing information,
and accepted orders continue to depend on the former ingredient record.

The specific intervention is dependency-aware change control, not a consumer
food scanner or an AI declaration that a meal is safe.

### Complete minimum workflow

1. Receive a supplier substitution message and a legible ingredient label.
2. AI proposes the ingredient identity and changed statements, with evidence
   locations; an unclear label produces an unresolved record.
3. Software follows explicitly recorded ingredient → recipe → menu/order links.
   Affected dispatches are held under a previously chosen operating policy.
4. A responsible kitchen operator checks the actual packaging and corrects or
   confirms the proposed facts. The human chooses to reject the substitution,
   withdraw affected meals, or use an already documented alternative.
5. Update the controlled menu/dispatch records and create the exact kitchen
   actions. Re-read the external records before reporting completion.
6. A changed ingredient record invalidates earlier approvals. Retrying an action
   does not duplicate tasks; a failed integration leaves the hold visible.

Suggested scope: one kitchen, two recipes, five synthetic orders, one substituted
ingredient, one uncertain-label case. A human records physical checks; the app
must not pretend it has independently verified kitchen practices or cross-contact.
Absence of a listed allergen is not proof of absence or general food safety.

Suggested integrations: fastn → Google Sheets for ingredient/menu/dispatch
records; fastn → Trello for kitchen actions. The deployed app provides the
controlled dispatch screen and checks its current holds. Email is optional,
not a prerequisite for completion.

AI handles messy evidence extraction and a grounded impact explanation. The
dependency traversal, hold rules, version checks, and allowed transitions are
ordinary deterministic software. Multiple agents are unnecessary.

### Demonstration and distinction

Try to dispatch an order; introduce a changed label; show the affected dependency
paths and blocked dispatch; have the operator reject the substitution and choose
the previously documented alternative; show the records/tasks updated and the
appropriate dispatch restored. Any physical preparation confirmation is explicitly
human-attested. Do not imply that a digital status change alone made food safe.

Existing Nutritics documentation already describes allergen propagation through
recipes, labels, and digital menus. We cannot claim to invent that.
[Existing product documentation](https://en-gb.nutritics.com/en/support-center/allergen-management/).
The proposed distinction to test is incoming, unstructured substitution evidence
plus operational holds on already accepted orders, with verified resolution.
Whether small kitchens need this instead of existing software is unvalidated.

Estimated focused implementation: 7–10 elapsed hours with two capable builders,
familiar tooling, working account access, and scope held. This is a planning
estimate, not a delivery guarantee; integration approval delays are excluded.

Reject or rescope if it becomes a restaurant platform, nutrition advisor,
automatic recipe generator, universal allergen interpreter, or a claim of safety
certification. A static recipe graph and one explicit allergen example suffice.

## 2. Verified vendor-change desk — strongest direct financial stakes

### Evidence and existing solution

IC3 lists roughly $3 billion in reported business email compromise losses in
2025. This is a reported-loss category, not all invoice fraud or a forecast.
[IC3 summary](https://www.ic3.gov/Outreach/Brochures/ic3-brochure.pdf).

DOJ describes recovery of approximately $4.86 million taken from Dickinson Public
Schools in a BEC scheme, announced April 30, 2026.
[First-party incident report](https://www.justice.gov/usao-nd/pr/north-dakota-fbi-and-us-attorneys-office-recover-48-million-dollars-scammed-dickinson).

The FBI advises independently verifying account/payment procedure changes.
[FBI guidance](https://www.fbi.gov/how-we-can-help-you/common-frauds-and-scams/business-email-compromise).
Eftsure already provides vendor-change verification and approval workflows.
[Existing product](https://www.eftsure.com/vendor-management/).

### Proposed mechanism and workflow

The defect is an untrusted message becoming authoritative payment data. An
authentic sender or familiar thread cannot establish that a requested change is
authorized. AI should not label a bank account genuine.

Controlled mailbox request → extracted change with source evidence → compare
with protected vendor record → hold the affected payment-export entry → reviewer
uses a previously recorded independent contact and records the result → approve
or reject the exact change/version → update the vendor register if authorized →
generate a controlled export containing only permitted instructions → re-read
the register and record the disposition.

Use a synthetic vendor register and invoices. One teammate can enact the vendor
verification role and the other the finance role, with the test explicitly marked
as a simulation. Credentials and verification contacts must not come from the
suspect email. Version changes invalidate approval.

Integrations: fastn Gmail and Google Sheets. The outcome is an authorized payment
instruction/export, not a bank transfer or independent account-ownership check.
It only blocks exports that actually pass through this application. A bypass
outside the app remains outside its protection.

Estimated implementation: 6–9 focused elapsed hours under the same assumptions.
Its strongest demo is rejecting a convincing fraudulent change while processing
a legitimate, independently verified one. Biggest weakness: appearing to be an
ordinary approval form; stale-approval invalidation and protected contact
provenance must be real, not just described.

## 3. Secondhand product intake gate — best public-data footing

This sharpens the earlier recall idea; it is not a wholly new problem category.

CPSC says its e-commerce team searches for recalled products and has listings
removed. The agency supplies a public recall API in JSON/XML.
[Observed enforcement workflow](https://www.cpsc.gov/About-CPSC/Division-of-Field-Operations/FAQs-For-Buying-and-Selling-Products-Online),
[API documentation](https://www.cpsc.gov/Recalls/CPSC-Recalls-Application-Program-Interface-API-Information).

An Anker recall illustrates that model and qualifying serial numbers matter;
brand-name similarity alone is insufficient.
[Concrete recall](https://www.cpsc.gov/Recalls/2025/More-than-One-Million-Anker-Power-Banks-Recalled-Due-to-Fire-and-Burn-Hazards-Manufactured-by-Anker-Innovations).
There are established recall execution products, including Recall InfoLink.
[Existing product](https://www-origin.recallinfolink.com/why-recall-infolink).

The proposed user is a small US resale operator. Identity information is often
the missing link in the proposed scenario; its actual prevalence in that segment
has not been independently measured here.

Intake photo/description → proposed identity → retrieve relevant official notices
→ hold unclear or potentially affected units before listing → human checks model,
serial, and applicable notice → quarantine matching units or record the specific
review disposition → update inventory and intake task → demonstrate that the
controlled storefront refuses held units. No blanket 'safe product' certificate.

Scope: one product category, one or two official notices, ten synthetic inventory
units. Integrations: CPSC API plus fastn Sheets/Trello. Do not build an external
marketplace scraper, global regulatory engine, or manufacturer's remedy portal.
The hackathon cannot verify physical disposal or force independent marketplaces
to remove listings.

Estimated implementation: 7–10 focused elapsed hours. Strong demo: similar-looking
units receive different dispositions because model/serial evidence differs.
Unknown identity remains on hold. Weakness: may look like recall search unless
listing prevention and state verification are implemented.

## Directions screened out for this deadline

- Medicine shortage allocation and clinical referral closure: substantial impact,
  but operational access, human expertise, and real fulfillment exceed our current
  evidence and access. Do not promise stock delivery or completed treatment.
- General food redistribution and disaster-aid matching: matching is only part
  of the work; transport, consent, capacity, and confirmed receipt dominate
  whether rescue actually occurred. No partner network is available.
- Generic credential-leak response: real urgency, but existing GitGuardian
  documentation already covers human context, provider revocation, and subsequent
  validity checks. A new dashboard is not a new contribution; provider-specific
  rotation also introduces deadline risk.
  [2026 vendor research](https://blog.gitguardian.com/the-state-of-secrets-sprawl-2026-pr/),
  [Existing remediation workflow](https://docs.gitguardian.com/internal-monitoring/remediate/remediate-incidents).
- General contractor offboarding: existing BetterCloud templates already group
  cross-application revocation and guest approvals; broad admin permissions are
  a setup risk.
  [Existing workflow](https://www.bettercloud.com/monitor/saasops-workflows-bettercloud-templates/).

## What increases the odds of a strong submission

My recommendation is ingredient-change control for its visible dependency chain,
substantive human decision, and controlled dispatch outcome. Vendor change control
is the fallback for direct monetary stakes. This is a rubric-informed judgment,
not a prediction of winning or proof of an unserved market.

Before development, resolve the organizer approval/fastn discrepancy. Prove the
two account connections before investing in UI. Deploy a thin health-checked app
to Alternate Clouds early. Use one runtime, one small persistent database, and
explicit workflow states; a graph database and multi-agent framework are not
necessary. Persist action IDs and external results across restarts.

Acceptance demonstration: happy path; uncertain evidence held; a changed record
invalidating an old approval; an integration error remaining recoverable; safe
retry without duplicate external writes; independent read-back of final state.

Aim to finish the functional workflow overnight, reserve the morning for testing,
video, screenshots, participant-written LinkedIn content, submission PDF and
slides, and be ready to submit by noon. Deployment must remain on Alternate
Clouds. Respect the official October 17, 12:45 PM PKT freeze even if work slips.
