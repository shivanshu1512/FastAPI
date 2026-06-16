# Pydantic v2 — My Learning Notes

> Personal notes and practice code while learning **Pydantic v2** — the data validation library that powers FastAPI.
> Written as I explored each concept, one file at a time.

---

## 📁 Files in this Folder

| # | File | What I Learned |
|---|------|----------------|
| 1 | `01_pydantic_basics.py` | BaseModel, Field, Annotated, EmailStr, AnyUrl |
| 2 | `02_field_validator.py` | `@field_validator` — custom single-field rules |
| 3 | `03_model_validator.py` | `@model_validator` — cross-field business rules |
| 4 | `04_computed_fields.py` | `@computed_field` — auto-derived properties |
| 5 | `05_nested_models.py` | Nesting one model inside another |
| 6 | `06_serialisation.py` | `model_dump`, `model_dump_json`, include/exclude |

---

## 🚀 Setup

```bash
pip install pydantic[email]   # includes EmailStr and AnyUrl support
```

Run any file:

```bash
python pydantic/01_pydantic_basics.py
python pydantic/02_field_validator.py
# … and so on
```

---

## 📖 Quick Concept Notes

### 1 · What is Pydantic?
Pydantic lets you define **what your data should look like** using Python type hints.
It auto-validates, coerces, and documents your data — no manual if-else needed.

```python
class Patient(BaseModel):
    name: str
    age: int = Field(gt=0, lt=120)   # must be 1–119
    email: EmailStr                   # must be valid email
```

### 2 · Field Validators
Use `@field_validator` when you want custom logic on a **single field**:

```python
@field_validator("email")
@classmethod
def check_domain(cls, value: str) -> str:
    if "@gmail.com" in value:
        raise ValueError("Personal emails not allowed")
    return value
```

### 3 · Model Validators
Use `@model_validator` when the rule depends on **two or more fields together**:

```python
@model_validator(mode="after")
def require_emergency_for_seniors(self) -> Self:
    if self.age > 60 and "emergency" not in self.contact_details:
        raise ValueError("Seniors must have an emergency contact")
    return self
```

### 4 · Computed Fields
Add a read-only property that gets calculated automatically and shows up in serialisation:

```python
@computed_field
@property
def bmi(self) -> float:
    return round(self.weight / self.height ** 2, 2)
```

### 5 · Nested Models
Embed one model inside another for structured data:

```python
class Address(BaseModel):
    city: str
    pin: str

class Patient(BaseModel):
    name: str
    address: Address   # validated recursively
```

### 6 · Serialisation
Convert models to dict or JSON and back:

```python
patient.model_dump()                    # → Python dict
patient.model_dump_json(indent=2)       # → JSON string
patient.model_dump(exclude={"email"})   # exclude a field
patient.model_dump(exclude_none=True)   # skip None values
Patient.model_validate(raw_dict)        # dict  → model
Patient.model_validate_json(json_str)   # JSON  → model
```

---

## 📄 Resources I Used

- [Pydantic v2 Docs](https://docs.pydantic.dev/latest/)
- [FastAPI + Pydantic Guide](https://fastapi.tiangolo.com/tutorial/body/)
