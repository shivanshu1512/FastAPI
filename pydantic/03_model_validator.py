"""
03 — Model Validators
======================
Demonstrates cross-field validation using @model_validator.
Unlike @field_validator (which sees one field at a time), a model
validator receives the fully-constructed model and can enforce rules
that depend on multiple fields together.

Key concepts:
  - @model_validator(mode='after')  : runs after all fields are validated
  - @model_validator(mode='before') : runs on raw input dict before parsing
  - Cross-field rules               : e.g. age + contact_details together
"""

from pydantic import BaseModel, EmailStr, model_validator
from typing import List, Dict, Self


# ──────────────────────────────────────────────
# Model
# ──────────────────────────────────────────────

class Patient(BaseModel):
    """
    Patient model with a cross-field business rule:
    patients older than 60 MUST provide an 'emergency' contact.
    """

    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str] = []
    contact_details: Dict[str, str] = {}

    # ── model-level validator (runs AFTER all fields are set) ─────────
    @model_validator(mode="after")
    def require_emergency_contact_for_seniors(self) -> Self:
        """
        Enforce that elderly patients always have an emergency contact on file.
        Rule: age > 60  →  contact_details must contain the key 'emergency'.
        """
        if self.age > 60 and "emergency" not in self.contact_details:
            raise ValueError(
                f"Patient '{self.name}' is {self.age} years old. "
                "An 'emergency' contact is mandatory for patients over 60."
            )
        return self


# ──────────────────────────────────────────────
# Demo
# ──────────────────────────────────────────────

# ✅ Senior with emergency contact — valid
print("✅ Senior patient WITH emergency contact:")
senior_ok = Patient(
    name="Ramesh Gupta",
    email="ramesh@hdfc.com",
    age=65,
    weight=70.0,
    married=True,
    allergies=["sulfa"],
    contact_details={"phone": "9111111111", "emergency": "9222222222"},
)
print(senior_ok)

# ❌ Senior without emergency contact — invalid
print("\n❌ Senior patient WITHOUT emergency contact:")
try:
    Patient(
        name="Kamala Devi",
        email="kamala@icici.com",
        age=72,
        weight=55.0,
        married=False,
        contact_details={"phone": "9333333333"},   # no 'emergency' key
    )
except Exception as exc:
    print(exc)

# ✅ Young patient without emergency — valid (rule doesn't apply)
print("\n✅ Young patient without emergency contact (rule doesn't apply):")
young = Patient(
    name="Arjun Nair",
    email="arjun@hdfc.com",
    age=25,
    weight=68.0,
    married=False,
)
print(young)
