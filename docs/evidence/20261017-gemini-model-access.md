# Gemini model access preflight

October 17, 2026, approximately 08:42 PKT. Source parent: ab57124, before
application/model-adapter changes. Mode: live read-only discovery; no generation.

The key was read from Git-ignored `.env` and sent only as the `x-goog-api-key`
header to Google's model-list endpoint. No key value or response headers were printed.
Observed HTTP 200, selected model `gemini-3.8-flash`, available for `generateContent`.
The account's actual generation quota, structured-output behavior and interpretation
quality remain UNVERIFIED. No acceptance row is promoted to PASS by this discovery.

## Replay from repository root (PowerShell)

Requires the local virtual environment and `GEMINI_API_KEY` in private `.env`.

```powershell
@'
import httpx
from dotenv import dotenv_values
v = dotenv_values('.env')
assert v.get('GEMINI_API_KEY'), 'Set GEMINI_API_KEY privately in .env'
r = httpx.get('https://generativelanguage.googleapis.com/v1beta/models',
    headers={'x-goog-api-key': v['GEMINI_API_KEY']}, timeout=20)
print('HTTP status:', r.status_code)
if r.status_code == 200:
    names = [m['name'].removeprefix('models/') for m in r.json().get('models', [])
        if 'generateContent' in m.get('supportedGenerationMethods', [])]
    print('Selected model available:', v.get('BUGPROOF_MODEL') in names)
'@ | .venv\Scripts\python.exe -
```

Fastn discovery was not attempted: `FASTN_API_KEY` was not present in `.env`.
Organization slug supplied by the participant is private configuration context,
not proof of a project ID or connected Gmail/GitHub tools.
