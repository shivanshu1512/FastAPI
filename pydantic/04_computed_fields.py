"""
04 — Computed Fields
=====================
Demonstrates how to add read-only, derived attributes to a Pydantic
model using @computed_field + @property.

The computed value is:
  - NOT accepted as input (ignored if passed)
  - Automatically re-calculated from other fields
  - Included in serialisation (model_dump / model_dump_json)

Key concepts:
  - @computed_field  : marks a property as a Pydantic-managed field
  - @property        : makes it accessible as an attribute, not a method
  - Return type hint : required for Pydantic to infer the schema correctly
"""

from pydantic import BaseModel, EmailStr, computed_field
from typing import List, Dict, Literal


# ──────────────────────────────────────────────
# Model
# ──────────────────────────────────────────────

class Patient(BaseModel):
    """Patient model with auto-computed BMI and health verdict."""

    name: str
    email: EmailStr
    age: int
    weight: float   # kilograms
    height: float   # metres
    married: bool
    allergies: List[str] = []
    contact_details: Dict[str, str] = {}

    # ── computed field: BMI ───────────────────
    @computed_field  # type: ignore[misc]
    @property
    def bmi(self) -> float:
        """Body Mass Index = weight (kg) / height² (m²), rounded to 2 d.p."""
        return round(self.weight / (self.height ** 2), 2)

    # ── computed field: WHO weight category ──
    @computed_field  # type: ignore[misc]
    @property
    def weight_category(self) -> Literal["Underweight", "Normal", "Overweight", "Obese"]:
        """WHO BMI classification."""
        if self.bmi < 18.5:
            return "Underweight"
        if self.bmi < 25.0:
            return "Normal"
        if self.bmi < 30.0:
            return "Overweight"
        return "Obese"


# ──────────────────────────────────────────────
# Helper: apply a partial update and re-display
# ──────────────────────────────────────────────

def update_patient(patient: Patient, **updates) -> Patient:
    """
    Return a new Patient with selected fields updated.
    Computed fields (bmi, weight_category) are recalculated automatically.
    """
    current = patient.model_dump()
    current.update(updates)
    return Patient(**current)


# ──────────────────────────────────────────────
# Demo
# ──────────────────────────────────────────────

p = Patient(
    name="Divya Menon",
    email="divya@hdfc.com",
    age=30,
    weight=68.0,
    height=1.65,
    married=False,
    allergies=["latex"],
    contact_details={"phone": "9444444444"},
)

print("── Original patient ───────────────────────")
print(f"BMI             : {p.bmi}")
print(f"Weight Category : {p.weight_category}")
print(p.model_dump_json(indent=2))

# Simulate weight gain and see category change
p2 = update_patient(p, weight=92.0)
print("\n── After weight update (92 kg) ────────────")
print(f"BMI             : {p2.bmi}")
print(f"Weight Category : {p2.weight_category}")
