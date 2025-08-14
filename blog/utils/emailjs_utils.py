import os
import logging
from typing import Dict, Any

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

EMAILJS_URL = getattr(settings, "EMAILJS_URL", "https://api.emailjs.com/api/v1.0/email/send")
EMAILJS_SERVICE_ID = os.getenv("EMAILJS_SERVICE_ID", "")
EMAILJS_TEMPLATE_ID = os.getenv("EMAILJS_TEMPLATE_ID", "")
EMAILJS_USER_ID = os.getenv("EMAILJS_USER_ID", "")
EMAILJS_TIMEOUT = float(os.getenv("EMAILJS_TIMEOUT", "6.0"))


def _build_payload(name: str, email: str, message: str) -> Dict[str, Any]:
    return {
        "service_id": EMAILJS_SERVICE_ID,
        "template_id": EMAILJS_TEMPLATE_ID,
        "user_id": EMAILJS_USER_ID,
        "template_params": {
            "name": name,
            "email": email,
            "message": message,
        },
    }


def send_email_via_emailjs(name: str, email: str, message: str) -> bool:
 
    if not (EMAILJS_SERVICE_ID and EMAILJS_TEMPLATE_ID and EMAILJS_USER_ID):
        logger.warning("EmailJS not configured; skipping send.")
        return False

    try:
        payload = _build_payload(name, email, message)
        resp = requests.post(
            EMAILJS_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=EMAILJS_TIMEOUT,
        )
        if 200 <= resp.status_code < 300:
            return True

        logger.error("EmailJS error %s: %s", resp.status_code, resp.text[:500])
        return False

    except requests.Timeout:
        logger.error("EmailJS request timed out after %.1fs", EMAILJS_TIMEOUT)
        return False
    except requests.RequestException as exc:
        logger.exception("EmailJS request failed: %s", exc)
        return False

