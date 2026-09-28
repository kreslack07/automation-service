#!/usr/bin/env python
# Contact form backend stub for automation-service.
#
# Purpose:
#   Accept the same fields as the static landing page contact form
#   (email, company, scope), log them as JSON, and return 200.
#
# This is a stub, not a live service.
# It runs without platform credentials; when you later wire real
# storage/email/Slack hooks, you can swap the log line for real delivery.
#
# Run:
#   pip install fastapi uvicorn
#   uvicorn contact_api:app --host 127.0.0.1 --port 8000
#
# Endpoints:
#   POST /submit-contact
#   GET  /health

import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict

try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel, EmailStr
except ImportError as exc:
    raise SystemExit(
        "Missing dependencies: pip install fastapi pydantic[email] uvicorn"
    ) from exc

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("contact_api")

app = FastAPI(title="automation-service contact stub", version="0.1.0")


class ContactSubmission(BaseModel):
    email: EmailStr
    company: str = ""
    scope: str = ""


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "service": "automation-service-contact-stub"}


@app.post("/submit-contact")
def submit_contact(payload: ContactSubmission) -> Dict[str, Any]:
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "email": payload.email,
        "company": payload.company.strip(),
        "scope": payload.scope.strip(),
    }
    # TODO(live): replace this with real storage/email/CRM/Slack hooks when credentials exist.
    log.info("contact submission received: %s", json.dumps(record, ensure_ascii=False))

    return {
        "ok": True,
        "message": "Contact form submitted",
        "record": record,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
