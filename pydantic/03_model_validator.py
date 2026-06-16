"""
Model Validators — Rules That Span Multiple Fields
====================================================
Sometimes a rule can't be checked on a single field alone.
For example: "if the patient is older than 60, they MUST have an
emergency contact." That rule touches both `age` AND `contact_details`.

That's where @model_validator(mode="after") comes in — it runs
AFTER all individual fields have been validated, and I can access
the full model (self) to check cross-field conditions.

Note: the method must return `self` (or `Self` as a type hint).
"""

from pydantic import BaseModel, EmailStr, model_validator
from typing import List, Dict, Self


class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str] = []
    contact_details: Dict[str, str] = {}

    @model_validator(mode="after")
    def require_emergency_contact_for_seniors(self) -> Self:
        """
        Business rule I added:
        Any patient over 60 years old must have an 'emergency' key
        in their contact_details — hospital policy.
        """
        if self.age > 60 and "emergency" not in self.contact_details:
            raise ValueError(
                f"Patient '{self.name}' is {self.age} years old. "
                "An emergency contact is required for patients above 60."
            )
        return self


# ── Try it out ───────────────────────────────────────────────────────────────

print("✅ Senior WITH emergency contact — should work:")
senior_ok = Patient(
    name="Ramesh Gupta",
    email="ramesh@hdfc.com",
    age=65,
    weight=70.0,
    married=True,
    contact_details={"phone": "9111111111", "emergency": "9222222222"},
)
print(senior_ok)

print("\n❌ Senior WITHOUT emergency contact — should raise error:")
try:
    Patient(
        name="Kamala Devi",
        email="kamala@icici.com",
        age=72,
        weight=55.0,
        married=False,
        contact_details={"phone": "9333333333"},  # no emergency key!
    )
except Exception as exc:
    print(exc)

print("\n✅ Young patient — no emergency contact needed:")
young = Patient(
    name="Arjun Nair",
    email="arjun@hdfc.com",
    age=25,
    weight=68.0,
    married=False,
)
print(young)
