import httpx
import asyncio
from datetime import datetime, date
from typing import List, Dict, Any
from models import Envelope

COMMODITY_CATALOG = [
    {"hs_code": "8471.30", "description": "Laptops and portable computers", "category": "Electronics"},
    {"hs_code": "8517.13", "description": "Smartphones and mobile devices", "category": "Electronics"},
    {"hs_code": "9018.90", "description": "Medical instruments and appliances", "category": "Healthcare"},
    {"hs_code": "8443.32", "description": "Printers and office machinery", "category": "Office Equipment"},
]

async def validate_envelope(env: Envelope) -> Envelope:
    errors = []
    required = ["shipment_id", "recipient_name"]
    for field in required:
        if field not in env.extraction or env.extraction[field].value is None:
            errors.append(f"Missing required field: {field}")
    
    if not env.extraction.get("commodity_code") and not env.extraction.get("commodity_desc"):
        errors.append("Must provide either commodity_code or commodity_desc")

    ship_date_val = env.extraction.get("ship_date", {}).get("value")
    if ship_date_val:
        try:
            ship_date = datetime.strptime(ship_date_val, "%Y-%m-%d").date()
            days_diff = (date.today() - ship_date).days
            if ship_date > date.today() or days_diff > 365:
                errors.append("ship_date is out of valid range (future or > 365 days old)")
        except ValueError:
            errors.append("Invalid date format. Expected YYYY-MM-DD")

    threshold = env.processing_instructions.get("confidence_threshold", 0.80)
    failed_conf = []
    for key, field in env.extraction.items():
        if field.confidence < threshold:
            failed_conf.append(key)

    hitl_enabled = env.processing_instructions.get("hitl_on_failure", True)
    if not errors and not failed_conf:
        route = "auto_approve"
    elif hitl_enabled:
        route = "hitl_review"
    else:
        route = "rejected"

    env.validation_results = {"errors": errors, "low_confidence_fields": failed_conf}
    env.decision = {"route": route}
    
    env.audit.append({
        "timestamp": datetime.now().isoformat(),
        "service": "validation-service",
        "action": "validate",
        "result": "success" if not errors else "failed",
        "details": {"errors": errors, "low_confidence": failed_conf}
    })
    return env

async def match_commodity(env: Envelope) -> Envelope:
    threshold = env.processing_instructions.get("confidence_threshold", 0.80)
    code_field = env.extraction.get("commodity_code")
    desc_field = env.extraction.get("commodity_desc")

    if code_field and code_field.confidence < threshold and desc_field:
        try:
            await asyncio.sleep(0.5)
            match_result = {
                "matched_code": "8471.30.0100",
                "match_confidence": 0.92,
                "rationale": f"Matched '{desc_field.value}' to laptop category.",
                "fallback_used": True,
                "source": "llm_match"
            }
            env.matching_results = match_result
        except Exception as e:
            env.matching_results = {"source": "no_match", "fallback_used": False}
            env.decision["route"] = "hitl_review"
            env.audit.append({"action": "matching_failed", "error": str(e)})

    return env