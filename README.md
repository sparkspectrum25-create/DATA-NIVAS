# FRIDAY server

Backend application for the FRIDAY agents. It has no Android app and no launcher.

## Run locally
```
pip install -r requirements.txt
export FRIDAY_TOKEN=change-me-to-a-long-random-string
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
Docs: http://localhost:8000/docs

## Run tests
```
FRIDAY_TOKEN=x pytest -q
```

## Agents
- JARVIS: server status.
- FRIDAY: device registry and last status.
- EDITH: audit of your own devices' permission lists (`/audit/permissions`).
- DUM-E: cleanup plan from storage numbers (`/repair/plan`). Returns steps only, never deletes.
- Vision and Location: need `consent: true` on every request. No analyzer is wired in yet.
- ULTRON: dormant until the exact phrase "wake up, ultron".

## Important limits
- State is in memory. It resets on restart. Move it to a database before real use.
- Every protected route needs `Authorization: Bearer <FRIDAY_TOKEN>`. Without the token set, the server refuses requests.
- EDITH and DUM-E only give advice. Any action runs on the device, through its own consent and permissions.
