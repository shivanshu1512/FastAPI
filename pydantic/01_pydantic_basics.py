"""
Pydantic Basics — BaseModel, Field & Type Validation
=====================================================
When I first started learning FastAPI, I kept seeing Pydantic everywhere.
This file is my practice of the core building blocks:

Things I tried here:
  - BaseModel     : the base class every model inherits from
  - Field()       : add constraints (min, max, gt, lt) and docs to a field
  - Annotated     : cleaner way to attach Field metadata to a type
  - EmailStr      : validates proper email format automatically
  - AnyUrl        : validates proper URL format automatically
  - Optional      : fields that are not always required
"""

from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated


class Patient(BaseModel):
    """
    My first Pydantic model — a Patient with real-world constraints.
    Pydantic validates every field when I create an instance.
    """

    name: Annotated[
        str,
        Field(
            max_length=50,
            title="Patient Name",
            description="Full name of the patient, max 50 characters.",
            examples=["Aarav Sharma", "Priya Patel"],
        ),
    ]
    email: EmailStr                             # rejects "notanemail" automatically
    linkedin_url: AnyUrl                        # rejects "not-a-url" automatically
    age: int = Field(gt=0, lt=120)              # 1–119, raises error outside range
    weight: Annotated[float, Field(gt=0, strict=True)]  # strict=True: no int→float coercion
    married: Annotated[
        Optional[bool],
        Field(default=None, description="None = not recorded yet"),
    ]
    allergies: Optional[List[str]] = None
    contact_details: Dict[str, str] = {}


# ── Try it out ───────────────────────────────────────────────────────────────

patient_data = {
    "name": "Aarav Sharma",
    "email": "aarav@hdfc.com",
    "linkedin_url": "https://linkedin.com/in/aarav-sharma",
    "age": 28,
    "weight": 72.5,
    "married": False,
    "allergies": ["penicillin", "peanuts"],
    "contact_details": {"phone": "9876543210", "emergency": "9123456789"},
}

patient = Patient(**patient_data)
print(patient)
print(f"\nName  : {patient.name}")
print(f"Email : {patient.email}")
print(f"Age   : {patient.age}")
