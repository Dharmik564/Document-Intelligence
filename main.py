from fastapi import FastAPI, HTTPException
from models import Envelope
from services import validate_envelope, match_commodity

app = FastAPI(title="PrintDeed Document Intel")

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "doc-intel", "version": "1.0.0"}

@app.post("/validate")
async def validate(envelope: Envelope):
    return await validate_envelope(envelope)

@app.post("/match")
async def match(envelope: Envelope):
    return await match_commodity(envelope)

@app.post("/process")
async def process_full(envelope: Envelope):
    # Step 1: Validate
    envelope = await validate_envelope(envelope)
    
    # Step 2: Match if needed
    envelope = await match_commodity(envelope)
    
    return envelope