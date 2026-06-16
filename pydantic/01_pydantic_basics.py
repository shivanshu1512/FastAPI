"""
01 — Why Pydantic? Basic Model Definition
==========================================
Demonstrates how Pydantic replaces manual data validation with
a clean, declarative approach using BaseModel and Field types.

Key concepts:
  - BaseModel           : base class for all Pydantic models
  - Field()             : add constraints and metadata to fields
  - Annotated           : attach Field metadata without changing the type
  - EmailStr / AnyUrl   : built-in string types with format validation
  - Optional            : mark a field as not required
"""

from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated


# ──────────────────────────────────────────────
# Model Definition
# ──────────────────────────────────────────────

class Patient(BaseModel):
    """Represents a patient with validated personal and medical data."""

    name: Annotated[
        str,
        Field(
            max_length=50,
            title="Patient Name",
            description="Full name of the patient (≤ 50 characters).",
            examples=["Aarav Sharma", "Priya Patel"],
        ),
    ]
    email: EmailStr                            # must be a valid email format
    linkedin_url: AnyUrl                       # must be a valid URL
    age: int = Field(gt=0, lt=120)             # 1–119 years
    weight: Annotated[float, Field(gt=0, strict=True)]  # kg, strict=no coercion
    married: Annotated[
        Optional[bool],
        Field(default=None, description="Marital status; None means unknown."),
    ]
    allergies: Optional[List[str]] = None      # list of allergy names
    contact_details: Dict[str, str] = {}       # e.g. {"phone": "9876543210"}


# ──────────────────────────────────────────────
# Demo
# ──────────────────────────────────────────────

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
