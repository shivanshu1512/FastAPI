"""
Computed Fields — Auto-Derived Properties
==========================================
Instead of calculating BMI manually every time I use the model,
I can use @computed_field to make it a permanent part of the model.

The cool thing: Pydantic treats it like a real field —
it shows up in model_dump() and model_dump_json() automatically.
I never need to pass it as input; it's always calculated fresh.

I used this concept a lot in my FastAPI patient API (main.py).
"""

from pydantic import BaseModel, EmailStr, computed_field
from typing import List, Dict, Literal


class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float   # in kg
    height: float   # in metres
    married: bool
    allergies: List[str] = []
    contact_details: Dict[str, str] = {}

    @computed_field  # type: ignore[misc]
    @property
    def bmi(self) -> float:
        """
        BMI = weight(kg) / height²(m)
        Rounded to 2 decimal places.
        """
        return round(self.weight / (self.height ** 2), 2)

    @computed_field  # type: ignore[misc]
    @property
    def weight_category(self) -> Literal["Underweight", "Normal", "Overweight", "Obese"]:
        """
        WHO BMI classification:
        < 18.5  → Underweight
        < 25.0  → Normal
        < 30.0  → Overweight
        ≥ 30.0  → Obese
        """
        if self.bmi < 18.5:
            return "Underweight"
        if self.bmi < 25.0:
            return "Normal"
        if self.bmi < 30.0:
            return "Overweight"
        return "Obese"


def update_patient(patient: Patient, **changes) -> Patient:
    """
    Helper I wrote to partially update a patient.
    Since computed fields recalculate automatically, bmi and
    weight_category will always reflect the latest values.
    """
    data = patient.model_dump()
    data.update(changes)
    return Patient(**data)


# ── Try it out ───────────────────────────────────────────────────────────────

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

print("── Original ─────────────────────────────────")
print(f"BMI             : {p.bmi}")
print(f"Weight Category : {p.weight_category}")

print("\n── After gaining weight (92 kg) ─────────────")
p2 = update_patient(p, weight=92.0)
print(f"BMI             : {p2.bmi}")
print(f"Weight Category : {p2.weight_category}")

print("\n── Full JSON output ─────────────────────────")
print(p.model_dump_json(indent=2))
