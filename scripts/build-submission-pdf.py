"""Build the private submission draft; optional private JSON supplies missing facts.

Run with bundled Python. Never commit the private JSON or a PDF containing contacts/login.
"""
import json
from pathlib import Path
from xml.sax.saxutils import escape
from PIL import Image as PILImage
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/pdf'
OUT.mkdir(parents=True, exist_ok=True)
PRIVATE = ROOT / '.tools/submission-details.json'
data = json.loads(PRIVATE.read_text(encoding='utf-8')) if PRIVATE.exists() else {}
for name, file in [('Arial', 'arial.ttf'), ('ArialBold', 'arialbd.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(Path('C:/Windows/Fonts') / file)))
blue, ink, cream = map(HexColor, ['#1000ed', '#222222', '#f8f5ef'])
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyCustom', fontName='Arial', fontSize=10.3, leading=15, textColor=ink, spaceAfter=9))
styles.add(ParagraphStyle(name='SectionCustom', fontName='ArialBold', fontSize=17, leading=22, textColor=blue, spaceBefore=15, spaceAfter=12))
styles.add(ParagraphStyle(name='TitleCustom', fontName='ArialBold', fontSize=28, leading=32, textColor=blue, spaceAfter=10))
styles.add(ParagraphStyle(name='SmallCustom', fontName='Arial', fontSize=8.7, leading=13, textColor=ink, spaceAfter=7))
styles.add(ParagraphStyle(name='WhiteCustom', fontName='ArialBold', fontSize=12, leading=17, textColor=white))
header = ROOT / 'tmp/pdfs/submission-header.png'
PILImage.open(ROOT / 'tmp/pdfs/handbook-page9.png').crop((45,25,735,88)).save(header)
W,H = 595.276,841.89

def page(c, doc):
    c.setFillColor(cream); c.rect(0,0,W,H,fill=1,stroke=0)
    c.drawImage(str(header),40,H-67,width=W-80,height=47,mask='auto')
    c.setFillColor(HexColor('#f1e2d4')); c.rect(0,0,W,23,fill=1,stroke=0)
    c.setFillColor(ink); c.setFont('Arial',8)
    c.drawString(43,35,'BUGPROOF  /  AGENTIKA 2.0  /  NASCON 2026')
    c.drawRightString(W-43,35,str(doc.page))

def p(text, small=False):
    return Paragraph(text, styles['SmallCustom' if small else 'BodyCustom'])
def title(text): return Paragraph(text,styles['TitleCustom'])
def section(text): return Paragraph(text,styles['SectionCustom'])
def val(key): return escape(str(data.get(key) or 'PENDING - participant to supply'))
def field(label, key): return p(f'<b>{label}</b><br/>{val(key)}')
def link(label,url):
    safe=escape(url,{'"':'&quot;'})
    return p(f'<b>{label}</b><br/><link href="{safe}" color="#1000ed">{safe}</link>',True)
def img(path,maxw,maxh):
    im=PILImage.open(path); scale=min(maxw/im.width,maxh/im.height)
    return Image(str(path),width=im.width*scale,height=im.height*scale,hAlign='LEFT')
def notice(text):
    t=Table([[Paragraph(text,styles['WhiteCustom'])]],colWidths=[W-86]);
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),blue),('TOPPADDING',(0,0),(-1,-1),12),('BOTTOMPADDING',(0,0),(-1,-1),12),('LEFTPADDING',(0,0),(-1,-1),14)]));return t

story=[title('BugProof'),p('Team submission | Human + AI: Better Together'),
notice('DRAFT - video, social links and Discord proof pending'),
section('1. Team details'),field('Team name','team_name')]
members=[]
for n in (1,2):
    members.append([p(f'<b>Member {n}</b>'),p(f'<b>Name:</b> {val(f"member{n}_name")}<br/><b>Email:</b> {val(f"member{n}_email")}<br/><b>Discord:</b> {val(f"member{n}_discord")}')])
t=Table(members,colWidths=[72,W-158]);t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,-1),0.5,HexColor('#ddd6ce')),('BOTTOMPADDING',(0,0),(-1,-1),8)]));story.append(t)
story += [Spacer(1,8),field('WhatsApp team contact','whatsapp'),section('2. About your project'),
p('<b>One-line pitch</b><br/>Turn a support report into reproducible API evidence, a human-approved engineering issue and a verified reporter reply.'),
p('<b>Problem and users</b><br/>Support engineers receive bug reports with uncertain facts and incomplete reproduction steps. Developers need concrete evidence, while customers need a clear response. BugProof connects these steps in one controlled workflow.'),
p('<b>Where the human comes in</b><br/>AI proposes and runs a bounded investigation. The support engineer can correct the expected behavior, choose escalation or clarification, or reject publication. Only approval of the exact saved issue and reply authorizes external actions.'),
p('<b>Stack</b><br/>Custom Python/FastAPI code, SQLite, server-rendered Jinja UI; Gemini 3.8 Flash structured proposals; fastn MCP connecting Gmail and GitHub; isolated HTTP order-test API. Hosted on Alternate Clouds; image built remotely through GitHub Actions.',True),PageBreak(),
title('Links and access'),section('3. Required links')]
live='https://alternate-graceful-plain-7359-docker-app.alternatefutures.ai'
story += [link('Live Alternate Clouds deployment',live),link('Accessible GitHub repository','https://github.com/M-Abdullah07/Bugproof')]
for label,key in [('2-3 minute demo video','demo_video'),('Original LinkedIn post','linkedin_post'),("Teammate's LinkedIn reshare",'linkedin_reshare')]:
    story.append(link(label,data[key]) if data.get(key) else field(label,key))
story += [p('<b>X / Twitter</b><br/>Optional; not included.'),section('Access for judges'),p('<b>Username:</b> Not required; password-only demo login.'),field('Dedicated demo password','demo_password'),p('Dedicated competition demo access only. No API keys, OAuth tokens or personal credentials are included.',True),section('What judges can verify'),
p('Faulty retry behavior stores two distinct orders; the corrected build stores one. Missing facts lead to clarification rather than invented evidence. The human controls disposition and publication. Delivery is complete only after the issue and original-thread reply are read back.'),
link('Verified demo engineering issue','https://github.com/M-Abdullah07/Bugproof/issues/3'),PageBreak(),title('Proof screenshots'),section('4. Proof screenshots'),p('<b>Alternate Clouds deployment</b><br/>BugProof Live is Active on Alternate Clouds. The dashboard shows the deployed image and public network endpoint.'),img(ROOT/'docs/evidence/images/ui-cloud-live.png',W-86,300),Spacer(1,12),p('<b>Alternate Futures Discord - both teammates</b>')]
for n in (1,2):
    key=f'member{n}_discord_screenshot'
    if data.get(key): story += [p(f'Member {n}',True),img(Path(data[key]),W-86,180)]
    else: story.append(p(f'Member {n}: PENDING - attach a screenshot visibly proving membership in the Alternate Futures server.',True))
story += [PageBreak(),title('Confirmations'),section('5. Confirm before submitting'),
p('<b>Participant confirmation required</b><br/>We wrote our LinkedIn post ourselves. Only grammar-only tools were used.'),
p('<b>Verified</b><br/>Our project is deployed on Alternate Clouds.'),
p('<b>Final participant check required</b><br/>No API keys or personal or production passwords appear in our repository, video or screenshots. The dedicated demo login is for judges only.'),
p('<b>Verified credits; final artifact review required</b><br/>Third-party code and development tools are credited in the repository.'),
p('<b>Participant commitment required</b><br/>We will not change our code or deployment after 12:45 PM PKT on October 17, 2026, and will keep the deployment running until the closing ceremony.'),
section('Implementation evidence'),p('36 deterministic tests passed. Live Gemini and fastn Gmail/GitHub runs completed escalation and clarification. A hosted container restart preserved completed provider IDs and approval. Tests use synthetic reports and an isolated API; this is not a claim of production payment diagnosis.',True),
img(ROOT/'docs/evidence/images/ui-live-case.png',W-86,190),Spacer(1,10),
link('Third-party credits','https://github.com/M-Abdullah07/Bugproof/blob/main/CREDITS.md'),
p('UI source and deployed application image: 55121985153118d1b605a4991674d170d54da25c. Subsequent repository changes are documentation only.',True)]
path=OUT/'BugProof-Agentika-Submission-DRAFT.pdf'
SimpleDocTemplate(str(path),pagesize=(W,H),rightMargin=43,leftMargin=43,topMargin=92,bottomMargin=55,title='BugProof - Agentika 2.0 Submission Draft',author='BugProof team').build(story,onFirstPage=page,onLaterPages=page)
print(path)
