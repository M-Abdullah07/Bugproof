import asyncio,base64,json,logging
from email.message import EmailMessage
from bugproof.config import Settings
from bugproof.integrations.fastn import Fastn
import sys
if "--allow-live" not in sys.argv: raise SystemExit("Explicit --allow-live required; sends only self-addressed synthetic reports")
logging.disable(logging.CRITICAL)
REPORTS={"retry":"Our order request returned HTTP 503 after a transient failure. We retried the identical payload with the same retry identifier, order-retry-42. Two distinct order records appeared. We expected only one order. Please investigate the duplicate orders.","missing":"Two orders appeared after our checkout request. Can you investigate? We do not yet have details of the failed response or retry identifier.","paraphrase":"After the create-order endpoint failed with 503, our client submitted exactly the same order data again, reusing retry identifier repeat-789. We then saw two order records instead of one."}
async def main():
 s=Settings.from_environment(); f=Fastn(s)
 for label,text in REPORTS.items():
  mid=f"bugproof-seed-v1-{label}@bugproof.demo"
  existing=await f.action("messages",{'q':f'subject:"BugProof Demo" subject:"{label} investigation" from:{s.mailbox}',"maxResults":1})
  if existing.get("messages"):
   print(json.dumps({"scenario":label,"existing":True}),flush=True); continue
  m=EmailMessage(); m["From"]=s.mailbox;m["To"]=s.mailbox;m["Subject"]="[BugProof Demo] "+label+" investigation";m["Message-ID"]="<"+mid+">";m["X-BugProof-Seed"]=label
  m.set_content("Synthetic report for the Agentika demonstration. No real customer or payment is involved.\n\n"+text)
  r=await f.action("send",{"raw":base64.urlsafe_b64encode(m.as_bytes()).decode(),"threadId":""})
  read=await f.get_message(r["id"])
  print(json.dumps({"scenario":label,"sent_and_read_back":read.get("id")==r["id"],"thread_id":r.get("threadId")}),flush=True)
asyncio.run(main())
