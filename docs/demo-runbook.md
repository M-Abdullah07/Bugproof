# BugProof participant handoff

Live: https://alternate-graceful-plain-7359-docker-app.alternatefutures.ai/login

Use `BUGPROOF_DEMO_PASSWORD` from the original workspace's private `.env`.
Give your teammate/judges the dedicated demo password privately; never share the
Gemini or fastn credentials. No additional account is needed to operate the app.

## Understand the workflow

1. **Check demo inbox** imports controlled Gmail reports through fastn.
2. **Investigate** asks Gemini for a grounded, bounded test plan. A fixed runner
   performs actual HTTP requests against the labeled isolated order service.
3. Inspect the source, expected count, observed order IDs and trace. The faulty
   service stores an order then returns 503; retry creates another. The corrected
   service recognizes the retry key and returns the original order.
4. Change the expected count or disposition if needed, then **Save edits**.
   Rejection prevents publication. Approval authorizes only the exact saved actions.
5. **Publish / reconcile approved actions** creates/read-verifies an engineering
   issue before sending/read-verifying the original-thread reply. Existing verified
   actions are reused. Uncertain sends require a read-only check, never blind retry.

This demonstrates support-to-engineering handoff with synthetic evidence, not a
production payment incident or an automatic code fix.

## Record a 2–3 minute video

- 0:00–0:20: show a support report: a failed request was retried and produced two orders.
- 0:20–1:00: investigate; point to the actual trace, build and distinct order IDs.
- 1:00–1:40: explain the human decision; edit/save an expectation or disposition,
  inspect the exact issue/reply, then approve deliberately.
- 1:40–2:15: publish; open the verified issue and original Gmail thread.
- 2:15–2:45: show corrected replay yields one order and incomplete reports require
  clarification. State the controlled-lab limit and mandatory Alternate Clouds hosting.

Existing cloud cases: retry `963d31a56ba9462eb13bba3a5cc8d428` already completed
[issue #3](https://github.com/M-Abdullah07/Bugproof/issues/3); missing-information
`5d95ede2dde043c2bf4ed83767f48939` already sent clarification; paraphrase
`cd5024185ed8488687c70eb057f8fdb3` has a corrected one-order run awaiting review.
Use that paraphrase case for a fresh human-controlled escalation after replaying
the faulty build. If reusing a completed case, explain its existing issue rather
than presenting a reused action as a new send. Keep all writes in controlled accounts.

## Submission remains participant work

Prepare the required PDF with both participants' details, live URL, accessible
repository, private demo login, 2–3 minute video, Discord membership screenshots,
[deployment screenshot](evidence/images/alternate-clouds.png), original LinkedIn
post and teammate reshare. Participants must write social posts themselves;
AI assistance is grammar-only. Required hashtags and full checklist are in the
[judge scorecard](judge_scorecard.md). Confirm submission destination/current updates.

Prepare finalist slides now: exactly five minutes, PDF due before 4 PM PKT if selected.
Submit by **12:45 PM PKT October 17**; target noon. Record the final repository
commit and deployed image from [deployment evidence](evidence/20261017-deployment.md).
Stop code/deployment changes at cutoff and keep the service running until closing.

## Operating limits

- Keep local OAuth apps/probes stopped; cloud `/data` owns the rotating tokens and SQLite.
- A GitHub push alone does not replace the cloud image. Current image is recorded
  in deployment evidence; docs/test-only commits require no rebuild.
- Do not delete/recreate the live service or its persistent volume during judging.
- Health is `/healthz`. Provider outages/quota remain possible; show errors honestly.
- 36 tests and hosted process restart passed; physical provider migration was not tested.

Latest UI/live proof: [UI record](evidence/20261017-ui.md). Full redeployment
migrated providers and reset cases; Gmail intake restored them with new IDs above.
Keep this active deployment running; only container-process restart durability
was proved. Pending redundant provider jobs require support attention.

For recording, open a fresh Incognito window or hard-refresh if the old green
stylesheet appears. The new design has a navy header, lime b. mark and blue controls.
