"""Human review owns disposition and exact payload approval."""
import hashlib
import json

from bugproof.experiments import evaluate


def fingerprint(case):
    binding={"case":case["id"],"revision":case["source_revision"],"version":case["version"],"state":case["state"]}
    return hashlib.sha256(json.dumps(binding,sort_keys=True).encode()).hexdigest()


def draft(case, settings, disposition=None, expected_count=1):
    state=case["state"]
    proposal=state.get("proposal",{})
    evidence=state.get("evidence",{})
    disposition=disposition or ("escalate" if evidence.get("outcome")=="reproduced_discrepancy" else "qualified" if evidence.get("complete") else "clarify")
    if disposition not in ("escalate","clarify","qualified"):
        raise ValueError("Choose an available disposition")
    if disposition in ("escalate","qualified") and not evidence.get("complete"):
        raise ValueError("Complete experimental evidence is required for this disposition")
    observation=f"Observed {len(evidence.get('orders',[]))} distinct order(s); expected {expected_count}."
    issue_body=(f"Synthetic BugProof demo — not a production incident.\n\n"
        f"Claim: {proposal.get('claim','Uninterpreted report')}\n\n"
        f"Expected: {expected_count} order(s) after identical sequential same-key retries.\n"
        f"Observation: {observation}\nEnvironment: isolated orders-lab; build {evidence.get('build','not run')}.\n"
        f"Run: {evidence.get('run_id','not run')}; fixture: {evidence.get('fixture','not run')}.\n\n"
        f"Synthetic inputs and actual HTTP trace:\n```json\n{json.dumps(evidence.get('trace',[]),indent=2)}\n```\n\n"
        f"Observed order IDs: {', '.join(o['id'] for o in evidence.get('orders',[]))}\n\n"
        "Limits: synthetic inputs; no payments, customer production, root cause or fix verified.")
    if disposition=="clarify":
        reply=proposal.get("question") or "Could you share the retry identifier behavior, whether the same payload was retried, and the original failed response?"
    else:
        reply=f"We tested your reported retry pattern in our isolated synthetic API ({evidence.get('build')}). {observation} This does not establish what happened in your production environment."
        if disposition=="escalate":
            reply+=" We are handing the recorded evidence to engineering: {{issue_url}}"
        else:
            reply+=" We have not dismissed your report. Please share any conditions that differ from this test."
    existing=next((a["result"].get("url") for a in case.get("actions",[]) if a["kind"]=="issue" and a["status"]=="done" and a.get("result")),None)
    return {"disposition":disposition,"expected_count":expected_count,"recipient":settings.mailbox,"repository":settings.repository,"existing_issue":existing,"issue_title":"[BugProof Demo] Duplicate orders after retry","issue_body":issue_body if disposition=="escalate" else "","reply":reply}


def revise(case, settings, values):
    expected=int(values.get("expected_count",1))
    if not 0 <= expected <= 5:
        raise ValueError("Expected order count must be between zero and five")
    preview=draft(case,settings,values.get("disposition"),expected)
    previous=case["state"].get("preview",{})
    changed_decision=expected!=previous.get("expected_count") or preview["disposition"]!=previous.get("disposition")
    for field,limit in (("issue_title",200),("issue_body",18000),("reply",6000)):
        if field in values:
            text=values[field]
            if changed_decision and text==previous.get(field):
                continue  # Regenerate unchanged boilerplate for the human's new decision.
            if not isinstance(text,str) or len(text)>limit:
                raise ValueError(f"Invalid {field}")
            preview[field]=text
    if not preview["reply"].strip() or (preview["disposition"]=="escalate" and (not preview["issue_title"].strip() or not preview["issue_body"].strip() or "{{issue_url}}" not in preview["reply"])):
        raise ValueError("Escalation requires an issue title/body and the {{issue_url}} placeholder in its reply")
    state={**case["state"],"preview":preview,"status":"ready_for_review"}
    if state.get("evidence"):
        state["outcome"]=evaluate(state["evidence"],expected)
    return state
