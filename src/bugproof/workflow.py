"""Case orchestration; proposals do not acquire publication authority."""
from bugproof.proposals import validate_proposal
from bugproof.review import draft


class Workflow:
    def __init__(self, storage, settings, integrations, proposer):
        self.storage=storage
        self.settings=settings
        self.integrations=integrations
        self.proposer=proposer

    async def intake(self):
        results=[]
        for source in await self.integrations.intake():
            case_id,changed=self.storage.ingest(self.settings.mailbox,source["thread_id"],source)
            results.append({"id":case_id,"changed":changed})
        return results

    async def investigate(self, case_id, build, runner):
        case=self.storage.case(case_id)
        # Persist intent before network work. A restart leaves a visible interrupted run.
        self.storage.save_state(case_id,{"status":"investigating","build":build},case["version"],"investigation_started")
        case=self.storage.case(case_id)
        version=case["version"]
        try:
            proposal=validate_proposal(await self.proposer.propose(case["source"]),case["source"])
            state={"status":"ready_for_review","proposal":proposal}
            if proposal["classification"]=="supported":
                state["evidence"]=await runner.run(proposal,build)
                state["outcome"]=state["evidence"]["outcome"]
                if not state["evidence"]["complete"]:
                    state["status"]="execution_error"
            else:
                state["outcome"]=proposal["classification"]
            case["state"]=state
            state["preview"]=draft(case,self.settings)
        except Exception as exc:
            state={"status":"proposal_error","error":str(exc) if isinstance(exc,ValueError) else type(exc).__name__}
        self.storage.save_state(case_id,state,version,"investigation_result")
        return self.storage.case(case_id)
