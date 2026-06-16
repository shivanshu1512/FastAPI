"""
Field Validators — Custom Per-Field Rules
==========================================
I learned that Pydantic's built-in types (EmailStr, int, float) handle
format and range — but sometimes I need my OWN business logic.

That's where @field_validator comes in. It lets me write a function
that runs on a specific field after the basic type check passes.

Two validators I wrote here:
  1. validate_email_domain  — only allow corporate email addresses
  2. capitalise_name        — auto title-case the patient's name
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Dict, Optional, Annotated


# Only these corporate domains are accepted in my system
ALLOWED_DOMAINS = frozenset({"hdfc.com", "icici.com", "sbi.co.in"})


class Patient(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=50)]
    email: EmailStr
    age: Annotated[int, Field(gt=0, lt=120)]
    weight: Annotated[float, Field(gt=0)]
    married: bool
    allergies: List[str] = []
    contact_details: Dict[str, str] = {}

    @field_validator("email")
    @classmethod
    def validate_email_domain(cls, value: str) -> str:
        """
        I only want patients from partner institutions.
        Extract the domain and check against my allowed list.
        """
        domain = value.split("@")[-1].lower()
        if domain not in ALLOWED_DOMAINS:
            raise ValueError(
                f"'{domain}' is not an accepted domain. "
                f"Allowed: {', '.join(sorted(ALLOWED_DOMAINS))}"
            )
        return value

    @field_validator("name")
    @classmethod
    def capitalise_name(cls, value: str) -> str:
        """
        Normalise the name — strip whitespace and title-case it.
        e.g. "  ravi mehta  " → "Ravi Mehta"
        """
        return value.strip().title()


# ── Try it out ───────────────────────────────────────────────────────────────

print("✅ Valid patient (corporate email):")
p = Patient(
    name="ravi mehta",          # will be cleaned to "Ravi Mehta"
    email="ravi@hdfc.com",
    age=32,
    weight=74.0,
    married=True,
    allergies=["aspirin"],
    contact_details={"phone": "9000000001"},
)
print(p)

print("\n❌ Invalid email domain — should raise an error:")
try:
    Patient(
        name="Sneha Iyer",
        email="sneha@gmail.com",   # personal email, not allowed
        age=27,
        weight=58.0,
        married=False,
    )
except Exception as exc:
    print(exc)
