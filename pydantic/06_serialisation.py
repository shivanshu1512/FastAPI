"""
Serialisation — Exporting Models to Dict & JSON
================================================
Once I have a Pydantic model, I often need to:
  - Send it as a JSON response (FastAPI does this automatically)
  - Save it to a file or database
  - Log only certain fields (hide sensitive ones like email)

Pydantic v2 has great built-in tools for all of this.

Things I practiced:
  - model_dump()              → Python dict
  - model_dump_json()         → JSON string
  - include / exclude         → pick specific fields
  - exclude_none              → skip fields that are None
  - model_validate()          → rebuild a model from a dict
  - model_validate_json()     → rebuild a model from a JSON string
"""

from pydantic import BaseModel
from typing import Optional


class Address(BaseModel):
    city: str
    state: str
    pin: str


class Patient(BaseModel):
    name: str
    gender: str = "Unknown"
    age: int
    weight: Optional[float] = None   # sometimes not recorded
    address: Address


# ── Build a sample patient ───────────────────────────────────────────────────

p = Patient(
    name="Nitish Kumar",
    gender="Male",
    age=35,
    address=Address(city="Gurgaon", state="Haryana", pin="122001"),
)
# Note: weight is None (not provided)

# ── 1. Full dict ─────────────────────────────────────────────────────────────
print("1. Full dict:")
print(p.model_dump())

# ── 2. Full JSON (pretty printed) ────────────────────────────────────────────
print("\n2. JSON (indented):")
print(p.model_dump_json(indent=2))

# ── 3. Only specific fields ───────────────────────────────────────────────────
print("\n3. Only name and age:")
print(p.model_dump(include={"name", "age"}))

# ── 4. Exclude a field ───────────────────────────────────────────────────────
print("\n4. Everything except gender:")
print(p.model_dump(exclude={"gender"}))

# ── 5. Skip None values ───────────────────────────────────────────────────────
print("\n5. Skip None fields (weight won't appear):")
print(p.model_dump(exclude_none=True))

# ── 6. Rebuild from dict ─────────────────────────────────────────────────────
print("\n6. Rebuild from raw dict:")
raw = {
    "name": "Priya Patel",
    "age": 22,
    "address": {"city": "Delhi", "state": "Delhi", "pin": "110001"},
}
p2 = Patient.model_validate(raw)
print(p2)

# ── 7. Round-trip: model → JSON → model ──────────────────────────────────────
print("\n7. Round-trip (model → JSON → model):")
json_str = p.model_dump_json()
p3 = Patient.model_validate_json(json_str)
print(p3)
