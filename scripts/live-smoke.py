"""Explicitly opted-in smoke through the authenticated app API.

Uses only configured self-addressed demo threads and the approved demo repository.
--publish exercises the approval endpoint as a preauthorized test operator;
it does not represent an unobserved human review as a product usability pass.
"""
import argparse
import json
from pathlib import Path
from urllib.parse import urlsplit

import httpx
from dotenv import dotenv_values

from bugproof.review import fingerprint


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--base-url",default="http://127.0.0.1:8000")
    parser.add_argument("--allow-live",action="store_true",required=True)
    parser.add_argument("--publish",action="store_true")
    parser.add_argument("--scenario",default="retry",choices=["retry","missing","paraphrase"])
    parser.add_argument("--build",default="faulty",choices=["faulty","corrected"])
    args=parser.parse_args()
    url=urlsplit(args.base_url)
    if url.scheme!="https" and url.hostname not in ("localhost","127.0.0.1"):
        raise SystemExit("Use HTTPS for a deployed smoke run")
    values=dotenv_values(".env")
    with httpx.Client(base_url=args.base_url,timeout=180,follow_redirects=True) as client:
        page=client.get("/login")
        token=page.text.split('name="csrf_token" value="')[1].split('"')[0]
        response=client.post("/login",data={"password":values["BUGPROOF_DEMO_PASSWORD"],"csrf_token":token})
        response.raise_for_status()
        session=client.get("/api/session");session.raise_for_status()
        client.headers["x-csrf-token"]=session.json()["csrf"]
        intake=client.post("/api/intake",json={}); intake.raise_for_status()
        selected=None
        for row in intake.json()["cases"]:
            result=client.get("/api/cases/"+row["id"]);result.raise_for_status()
            case=result.json()
            if case["source"]["messages"][0]["subject"]==f"[BugProof Demo] {args.scenario} investigation":
                selected=case
                break
        if not selected:
            raise SystemExit("No matching synthetic report. Seed the controlled mailbox first.")
        cid=selected["id"]
        run=client.post(f"/api/cases/{cid}/investigate",json={"fingerprint":fingerprint(selected),"build":args.build})
        run.raise_for_status()
        selected=run.json()
        summary={"build":session.json()["build"],"case_id":cid,"scenario":args.scenario,"target_build":args.build,"outcome":selected["state"].get("outcome"),"state":selected["state"].get("status"),"order_count":len(selected["state"].get("evidence",{}).get("orders",[])),"trace_statuses":[t["status"] for t in selected["state"].get("evidence",{}).get("trace",[])]}
        print(json.dumps(summary),flush=True)
        if selected["state"]["status"] not in ("ready_for_review",):
            raise SystemExit("Investigation did not reach review; no publication attempted")
        if args.publish:
            approval=client.post(f"/api/cases/{cid}/approve",json={"fingerprint":fingerprint(selected)})
            approval.raise_for_status()
            response=client.post(f"/api/cases/{cid}/publish",json={"approval_id":approval.json()["approval_id"]})
            response.raise_for_status()
            print(json.dumps({"publication":response.json()}),flush=True)
            if response.json().get("status") not in ("complete","awaiting_information"):
                raise SystemExit("Publication incomplete; inspect and reconcile before further writes")
        Path(".tools").mkdir(exist_ok=True)
        Path(".tools/live-smoke-last.json").write_text(json.dumps(summary,indent=2))


if __name__=="__main__":
    main()
