"""Durable action ownership, read-back and cautious reconciliation."""
import hashlib
import json
import time

from bugproof.review import fingerprint
from bugproof.integrations.fastn import ProviderRejected


class Publisher:
    def __init__(self, storage, provider, settings):
        self.storage=storage
        self.provider=provider
        self.settings=settings

    def verify_issue(self, result, preview, marker):
        expected_prefix=f"https://github.com/{self.settings.repository}/issues/"
        if not isinstance(result.get("number"),int) or result.get("html_url") != expected_prefix+str(result["number"]) or result.get("title")!=preview["issue_title"] or result.get("body","").replace("\r\n","\n")!=(preview["issue_body"]+f"\n\n<!-- {marker} -->").replace("\r\n","\n"):
            raise ValueError("Issue read-back does not match the approved payload/destination")
        return {"number":result["number"],"url":result["html_url"],"marker":marker}

    def verify_reply(self, result, source, text, marker):
        # Runtime provider implementation normalizes MIME; doubles must return the same shape.
        from bugproof.integrations.fastn import Fastn
        from email.utils import parseaddr
        headers={h["name"].lower():h["value"] for h in result.get("payload",{}).get("headers",[])}
        body=Fastn.text(result.get("payload",{})).replace("\r\n","\n").strip()
        expected=(text+f"\n\nBugProof delivery marker: {marker}").strip()
        if result.get("threadId") != source["thread_id"] or "SENT" not in result.get("labelIds",[]) or parseaddr(headers.get("to",""))[1].lower()!=self.settings.mailbox.lower() or body!=expected or headers.get("x-bugproof-action")!=marker:
            raise ValueError("Sent message read-back does not match the approved reply/thread/recipient")
        return {"id":result["id"],"thread_id":result["threadId"],"marker":marker}

    async def publish(self, case_id, approval_id):
        case=self.storage.case(case_id)
        bound=fingerprint(case)
        approval=self.storage.approval(case_id,approval_id,bound)
        preview=json.loads(approval["payload_json"])
        if preview!=case["state"].get("preview") or preview["recipient"]!=self.settings.mailbox or preview["repository"]!=self.settings.repository:
            raise ValueError("Destinations or payload have changed")
        issue=None
        kinds=["issue","reply"] if preview["disposition"]=="escalate" else ["reply"]
        for kind in kinds:
            # New evidence/review edits invalidate the authorization before every effect.
            current=self.storage.case(case_id)
            if fingerprint(current)!=bound:
                raise ValueError("Case changed; completed actions preserved, remaining actions stopped")
            identity=case_id+":issue" if kind=="issue" else case_id+":reply:"+hashlib.sha256(json.dumps({"revision":case["source_revision"],"preview":preview},sort_keys=True).encode()).hexdigest()[:24]
            marker="bugproof-"+hashlib.sha256(identity.encode()).hexdigest()[:32]
            text=preview["reply"].replace("{{issue_url}}",issue["url"] if issue else "")
            context={"source":case["source"],"preview":preview,"marker":marker,"reply_text":text}
            action,owned=self.storage.claim(current,approval_id,bound,identity,kind,context)
            if action["status"]=="done":
                result=json.loads(action["result_json"])
            else:
                if not owned and action["status"]=="running" and time.time()-action["updated"]<70:
                    return {"status":"publishing","detail":"Another request owns this action. Refresh shortly."}
                # A different unresolved reply must never be bypassed with edited content.
                if any(a["id"]!=identity and a["kind"]==kind and a["status"] in ("running","uncertain","created") for a in current["actions"]):
                    if owned:
                        self.storage.action_result(identity,"blocked",error="Resolve the earlier uncertain action first")
                    raise ValueError("Resolve the earlier uncertain action before a different payload")
                known=json.loads(action.get("result_json") or "null")
                try:
                    text=preview["reply"].replace("{{issue_url}}",issue["url"] if issue else "")
                    if not owned:
                        # Every existing attempt is reconciliation-only. Never resend on absence.
                        if kind=="issue":
                            found=await self.provider.get_issue(known["number"]) if known and known.get("number") else await self.provider.find_issue(marker)
                        else:
                            found=await self.provider.get_message(known["id"]) if known and known.get("id") else await self.provider.find_reply(marker)
                        if not found:
                            self.storage.action_result(identity,"uncertain",known,"No matching write found in bounded search; no resend performed")
                            return {"status":"uncertain","detail":"Remote outcome unresolved. Reconcile before retry; no duplicate sent."}
                    elif kind=="issue":
                        created=await self.provider.create_issue(preview["issue_title"],preview["issue_body"],marker)
                        known={"number":created["number"],"url":created.get("html_url"),"marker":marker}
                        self.storage.action_result(identity,"created",known)
                        found=await self.provider.get_issue(known["number"])
                    else:
                        created=await self.provider.send_reply(case["source"],text,marker)
                        known={"id":created["id"],"marker":marker}
                        self.storage.action_result(identity,"created",known)
                        found=await self.provider.get_message(known["id"])
                    result=self.verify_issue(found,preview,marker) if kind=="issue" else self.verify_reply(found,case["source"],text,marker)
                    self.storage.action_result(identity,"done",result)
                except Exception as exc:
                    if isinstance(exc,ProviderRejected) and known is None:
                        self.storage.action_result(identity,"failed",error="Provider explicitly rejected the write. Retry requires current approval.")
                        return {"status":"partial" if issue else "failed","detail":"Provider rejected this attempt before applying it. Correct the connection and retry with valid approval."}
                    self.storage.action_result(identity,"uncertain",known,"Provider outcome/read-back uncertain; reconcile before retry")
                    self.storage.event(case_id,"publication_error",{"kind":kind,"error_type":type(exc).__name__})
                    return {"status":"partial" if issue else "uncertain","detail":"Action outcome needs verification; successful actions are preserved."}
            if kind=="issue":
                issue=result
        result={"status":"awaiting_information" if preview["disposition"]=="clarify" else "complete","issue":issue,"case_version":case["version"],"source_revision":case["source_revision"]}
        self.storage.event(case_id,"publication_complete",result)
        return result

    async def reconcile(self, case_id):
        """Read-only remote checks remain available after approval expires/revises."""
        results=[]
        for action in self.storage.case(case_id)["actions"]:
            if action["status"] not in ("running","uncertain","created"):
                continue
            if action["status"]=="running" and time.time()-action["updated"]<70:
                results.append({"kind":action["kind"],"status":"publishing"})
                continue
            context=self.storage.action_snapshot(action["id"])
            if not context:
                results.append({"kind":action["kind"],"status":"uncertain","detail":"No durable payload snapshot; inspect provider manually"})
                continue
            known=action["result"]
            marker=context["marker"]
            try:
                if action["kind"]=="issue":
                    found=await self.provider.get_issue(known["number"]) if known and known.get("number") else await self.provider.find_issue(marker)
                    value=self.verify_issue(found,context["preview"],marker) if found else None
                else:
                    found=await self.provider.get_message(known["id"]) if known and known.get("id") else await self.provider.find_reply(marker)
                    value=self.verify_reply(found,context["source"],context["reply_text"],marker) if found else None
                if value:
                    self.storage.action_result(action["id"],"done",value)
                    results.append({"kind":action["kind"],"status":"done"})
                else:
                    self.storage.action_result(action["id"],"uncertain",known,"No matching write found; inspect provider manually. No resend authorized.")
                    results.append({"kind":action["kind"],"status":"uncertain"})
            except Exception:
                results.append({"kind":action["kind"],"status":"uncertain"})
        return {"checks":results,"external_writes":0}
