"""
Nested Models — Models Inside Models
======================================
Real-world data is structured, not flat. A patient has an address.
An address is its own thing with its own fields.

Instead of stuffing city/state/pin directly into Patient, I can create
a separate Address model and use it as a field type.

Pydantic validates nested models recursively — if Address fails,
the whole Patient creation fails with a clear error message.

I can also pass the nested model as a plain dict — Pydantic
converts it automatically. Very handy!
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional


class Address(BaseModel):
    """Represents an Indian postal address."""
    street: Optional[str] = None
    city: str
    state: str
    pin: str = Field(pattern=r"^\d{6}$", description="6-digit Indian PIN code")


class EmergencyContact(BaseModel):
    """Someone to call if the patient is in critical condition."""
    name: str
    relationship: str
    phone: str = Field(pattern=r"^\d{10}$", description="10-digit mobile number")


class Patient(BaseModel):
    """Full patient record — uses Address and EmergencyContact as nested models."""
    name: str
    gender: Literal["male", "female", "other"]
    age: int = Field(gt=0, lt=120)
    address: Address                               # nested model
    emergency_contact: Optional[EmergencyContact] = None  # optional nested


# ── Try it out ───────────────────────────────────────────────────────────────

# Build nested objects first, then compose
home = Address(street="12, MG Road", city="Gurgaon", state="Haryana", pin="122001")
ec   = EmergencyContact(name="Sunita Kumar", relationship="spouse", phone="9800000001")

p1 = Patient(name="Nitish Kumar", gender="male", age=35, address=home, emergency_contact=ec)

print("── Patient as dict ─────────────────────────")
print(p1.model_dump())

print("\n── Patient as JSON ─────────────────────────")
print(p1.model_dump_json(indent=2))

# Pydantic also accepts nested model as a plain dict — very convenient
p2 = Patient(
    name="Anita Joshi",
    gender="female",
    age=29,
    address={"city": "Pune", "state": "Maharashtra", "pin": "411001"},
)
print(f"\n── Patient 2 city : {p2.address.city}")
