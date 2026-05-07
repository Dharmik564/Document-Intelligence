from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class ExtractionField(BaseModel):
    value: Any
    confidence: float

class Envelope(BaseModel):
    envelope_id: str
    schema_version: str = "envelope-v1"
    tenant: Dict[str, str]
    document: Dict[str, Any]
    extraction: Dict[str, ExtractionField]
    processing_instructions: Dict[str, Any]
    validation_results: Optional[Dict[str, Any]] = None
    matching_results: Optional[Dict[str, Any]] = None
    decision: Optional[Dict[str, Any]] = None
    audit: List[Dict[str, Any]] = []