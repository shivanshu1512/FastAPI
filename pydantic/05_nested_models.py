"""
05 — Nested Models
===================
Demonstrates how to compose complex schemas by embedding one
Pydantic model inside another.

Key concepts:
  - Nested BaseModel    : a field whose type is itself a BaseModel
  - model_dump()        : serialize the full nested structure to dict
  - model_dump_json()   : serialize to JSON string
  - Validation cascade  : inner model is validated before the outer one
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional


# ──────────────────────────────────────────────
# Inner Models
# ──────────────────────────────────────────────

class Address(BaseModel):
    """Physical address with Indian postal format."""

    street: Optional[str] = None
    city: str
    state: str
    pin: str = Field(pattern=r"^\d{6}$", description="6-digit Indian PIN code")


class EmergencyContact(BaseModel):
    """Emergency contact details."""

    name: str
    relationship: str
    phone: str = Field(pattern=r"^\d{10}$", description="10-digit mobile number")


# ──────────────────────────────────────────────
# Outer Model
# ──────────────────────────────────────────────

class Patient(BaseModel):
    """Full patient record with nested address and emergency contact."""

    name: str
    gender: Literal["male", "female", "other"]
    age: int = Field(gt=0, lt=120)
    address: Address                              # nested model
    emergency_contact: Optional[EmergencyContact] = None  # optional nested


# ──────────────────────────────────────────────
# Demo
# ──────────────────────────────────────────────

# Build nested objects step by step
home_address = Address(
    street="12, MG Road",
    city="Gurgaon",
    state="Haryana",
    pin="122001",
)

ec = EmergencyContact(
    name="Sunita Kumar",
    relationship="spouse",
    phone="9800000001",
)

patient1 = Patient(
    name="Nitish Kumar",
    gender="male",
    age=35,
    address=home_address,
    emergency_contact=ec,
)

print("── Full patient (dict) ─────────────────────")
print(patient1.model_dump())

print("\n── Full patient (JSON) ─────────────────────")
print(patient1.model_dump_json(indent=2))

# Nested model can also be passed as a plain dict — Pydantic handles it
patient2 = Patient(
    name="Anita Joshi",
    gender="female",
    age=29,
    address={"city": "Pune", "state": "Maharashtra", "pin": "411001"},
)
print("\n── Patient 2 address city:", patient2.address.city)
