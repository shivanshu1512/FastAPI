"""
02 — Field Validators
======================
Demonstrates how to add custom per-field validation logic using
the @field_validator decorator.

Key concepts:
  - @field_validator      : validate (or transform) a single field
  - @classmethod          : field validators are always class methods
  - raise ValueError      : triggers a Pydantic ValidationError
  - return value          : must return the (possibly transformed) value
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Dict, Optional, Annotated


# ──────────────────────────────────────────────
# Allowed domains for institutional patients
# ──────────────────────────────────────────────

VALID_EMAIL_DOMAINS = frozenset({"hdfc.com", "icici.com", "sbi.co.in"})


# ──────────────────────────────────────────────
# Model
# ──────────────────────────────────────────────

class Patient(BaseModel):
    """Patient with a custom e-mail domain validator."""

    name: Annotated[str, Field(min_length=2, max_length=50)]
    email: EmailStr
    age: Annotated[int, Field(gt=0, lt=120)]
    weight: Annotated[float, Field(gt=0)]
    married: bool
    allergies: List[str] = []
    contact_details: Dict[str, str] = {}

    # ── field-level validator ──────────────────
    @field_validator("email")
    @classmethod
    def validate_email_domain(cls, value: str) -> str:
        """Accept only corporate e-mail addresses from known institutions."""
        domain = value.split("@")[-1].lower()
        if domain not in VALID_EMAIL_DOMAINS:
            raise ValueError(
                f"E-mail domain '{domain}' is not allowed. "
                f"Accepted: {', '.join(sorted(VALID_EMAIL_DOMAINS))}"
            )
        return value

    # ── field-level validator ──────────────────
    @field_validator("name")
    @classmethod
    def capitalise_name(cls, value: str) -> str:
        """Ensure the patient name is title-cased (e.g. 'ravi mehta' → 'Ravi Mehta')."""
        return value.strip().title()


# ──────────────────────────────────────────────
# Demo
# ──────────────────────────────────────────────

# ✅ Valid patient
valid_patient = Patient(
    name="ravi mehta",          # will be title-cased automatically
    email="ravi@hdfc.com",
    age=32,
    weight=74.0,
    married=True,
    allergies=["aspirin"],
    contact_details={"phone": "9000000001"},
)
print("✅ Valid patient created:")
print(valid_patient)

# ❌ Invalid domain — will raise ValidationError
print("\n❌ Attempting invalid email domain…")
try:
    Patient(
        name="Sneha Iyer",
        email="sneha@gmail.com",   # not an allowed domain
        age=27,
        weight=58.0,
        married=False,
    )
except Exception as exc:
    print(exc)
