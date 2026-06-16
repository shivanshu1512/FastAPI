"""
06 — Serialisation
===================
Demonstrates the various ways to convert a Pydantic model to
Python dicts and JSON strings, and how to control what gets included.

Key concepts:
  - model_dump()               : model → Python dict
  - model_dump_json()          : model → JSON string
  - include / exclude          : choose which fields to serialise
  - exclude_none / exclude_unset: skip None or un-set fields
  - model_validate() / model_validate_json(): deserialise back from dict/JSON
"""

from pydantic import BaseModel, Field
from typing import Optional


# ──────────────────────────────────────────────
# Models
# ──────────────────────────────────────────────

class Address(BaseModel):
    city: str
    state: str
    pin: str


class Patient(BaseModel):
    name: str
    gender: str = "Unknown"
    age: int
    weight: Optional[float] = None      # optional — may be None
    address: Address


# ──────────────────────────────────────────────
# Demo
# ──────────────────────────────────────────────

patient = Patient(
    name="Nitish Kumar",
    gender="Male",
    age=35,
    address=Address(city="Gurgaon", state="Haryana", pin="122001"),
)

print("── 1. Full dict ────────────────────────────")
print(patient.model_dump())

print("\n── 2. Full JSON (indented) ─────────────────")
print(patient.model_dump_json(indent=2))

print("\n── 3. Only name + age (include) ────────────")
print(patient.model_dump(include={"name", "age"}))

print("\n── 4. Everything except gender (exclude) ───")
print(patient.model_dump(exclude={"gender"}))

print("\n── 5. Skip None fields (exclude_none) ──────")
print(patient.model_dump(exclude_none=True))   # weight is None → omitted

print("\n── 6. Deserialise from dict (model_validate)──")
raw = {"name": "Priya", "age": 22, "address": {"city": "Delhi", "state": "Delhi", "pin": "110001"}}
p2 = Patient.model_validate(raw)
print(p2)

print("\n── 7. Deserialise from JSON string ─────────")
json_str = patient.model_dump_json()
p3 = Patient.model_validate_json(json_str)
print(p3)
