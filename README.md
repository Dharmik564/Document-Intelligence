````markdown
# Document Intelligence Platform - Senior AI Task

This project implements a production-ready slice of a document intelligence platform. It processes JSON Execution Envelopes by validating data, performing AI-driven commodity matching, and maintaining a transparent audit trail.

---

# 🛠 Tech Stack

- **Framework:** FastAPI (Python 3.11+)
- **Validation:** Pydantic v2
- **Client:** HTTPX (Async LLM calls)
- **Testing:** Pytest

---

# 🚀 Quick Start (Run in ≤ 3 Commands)

## 1. Install Dependencies

```bash
pip install fastapi uvicorn pydantic httpx pytest
```

## 2. Start the Service

```bash
uvicorn main:app --reload
```

## 3. Run Tests

```bash
pytest
```

---

# 📂 Project Structure

```bash
document-intelligence/
│
├── main.py
├── services/
│   ├── validation_service.py
│   ├── matching_service.py
│   └── audit_service.py
│
├── models/
│   └── envelope_models.py
│
├── tests/
│   └── test_api.py
│
└── README.md
```

---

# 🏗 Implemented Features

## ✅ Validation Service (`/validate`)

Verifies:

* Required fields:

  * `shipment_id`
  * `recipient_name`
* Confidence thresholds dynamically from the envelope
* `ship_date` range validation

---

## 🤖 AI Matching (`/match`)

Triggered when `commodity_code` confidence is low.

Features:

* Uses natural language fallback (`commodity_desc`)
* Matches against an in-memory HS code catalog
* Returns:

  * matched code
  * confidence
  * reasoning
  * HITL review when confidence is insufficient

---

## 🔄 Progressive Enrichment

The platform appends enriched data into:

* `validation_results`
* `matching_results`

without overwriting upstream extraction data.

This ensures complete traceability across the processing pipeline.

---

## 🧾 Audit Trail

Every service action is logged with:

* timestamp
* service name
* action performed
* failure reason (if any)

This provides explainability and operational transparency.

---

## 🛡 Reliability & Graceful Degradation

If the LLM/API fails or times out:

* the pipeline does not crash
* status automatically falls back to:

  ```json
  "hitl_review"
  ```

This guarantees resilient workflow execution.

---

# 📝 Design Notes

## The "Append-Only" Architecture

A major design decision was implementing a progressive enrichment model.

The original extraction envelope remains immutable and acts as the single source of truth.

Benefits:

* preserves chain of custody
* improves auditability
* simplifies debugging
* enables downstream traceability

This approach is especially important for logistics and compliance systems.

---

# ⚖ Trade-offs & Future Improvements

## LLM Mocking

For this submission:

* deterministic matching logic is used
* acts as a swap-point for:

  * OpenAI
  * Anthropic
  * Azure OpenAI

This keeps the implementation testable and reproducible.

---

## Scalability Improvements

Current implementation:

* HS code catalog stored in-memory

Production recommendation:

* move catalog to a Vector Database such as:

  * Pinecone
  * Weaviate
  * FAISS

Benefits:

* semantic similarity search
* scalability to thousands of HS codes
* faster retrieval before LLM refinement

---

# 📌 API Endpoints

| Endpoint    | Method | Description                  |
| ----------- | ------ | ---------------------------- |
| `/validate` | POST   | Validates execution envelope |
| `/match`    | POST   | Performs commodity matching  |
| `/health`   | GET    | Health check endpoint        |

---

# ✅ Example Response

```json
{
  "status": "success",
  "validation_results": {
    "shipment_id": "valid",
    "recipient_name": "valid"
  },
  "matching_results": {
    "commodity_code": "8471.30",
    "confidence": 0.91
  }
}
```

---

# 👨‍💻 Author

Dharmik Modi
Junior Python Developer / Backend Developer

```
```'