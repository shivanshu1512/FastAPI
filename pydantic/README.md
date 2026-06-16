# Pydantic Crash Course

> A clean, well-commented walkthrough of Pydantic v2 — the data validation library used by FastAPI under the hood.
> Source material: [campusx-official/pydantic-crash-course](https://github.com/campusx-official/pydantic-crash-course)

---

## 📁 Files in this Folder

| # | File | Concept Covered |
|---|------|-----------------|
| 1 | `01_pydantic_basics.py` | BaseModel, Field, Annotated, EmailStr, AnyUrl |
| 2 | `02_field_validator.py` | `@field_validator` — per-field custom rules |
| 3 | `03_model_validator.py` | `@model_validator` — cross-field rules |
| 4 | `04_computed_fields.py` | `@computed_field` — auto-derived properties |
| 5 | `05_nested_models.py` | Composing models inside models |
| 6 | `06_serialisation.py` | `model_dump`, `model_dump_json`, include/exclude |

---

## 🚀 Setup

```bash
pip install pydantic[email]   # includes EmailStr and AnyUrl support
```

Run any file individually:

```bash
python pydantic/01_pydantic_basics.py
python pydantic/02_field_validator.py
# … and so on
```

---

## 📖 Quick Concept Guide

### 1 · Why Pydantic?
Pydantic lets you declare **what your data should look like** using Python type hints — and it validates, coerces, and documents it automatically.

```python
class Patient(BaseModel):
    name: str
    age: int = Field(gt=0, lt=120)
    email: EmailStr
```

### 2 · Field Validators
Validate (or transform) a **single field** with custom logic:

```python
@field_validator("email")
@classmethod
def check_domain(cls, v: str) -> str:
    if "@gmail.com" in v:
        raise ValueError("Personal emails not allowed")
    return v
```

### 3 · Model Validators
Enforce rules that depend on **multiple fields together**:

```python
@model_validator(mode="after")
def require_emergency_for_seniors(self) -> Self:
    if self.age > 60 and "emergency" not in self.contact_details:
        raise ValueError("Emergency contact required for age > 60")
    return self
```

### 4 · Computed Fields
Add **read-only, derived attributes** that are auto-calculated and included in serialisation:

```python
@computed_field
@property
def bmi(self) -> float:
    return round(self.weight / self.height ** 2, 2)
```

### 5 · Nested Models
Embed one model inside another for **structured, hierarchical data**:

```python
class Address(BaseModel):
    city: str
    pin: str

class Patient(BaseModel):
    name: str
    address: Address   # nested — validated recursively
```

### 6 · Serialisation
Export models to dicts or JSON, with fine-grained control:

```python
patient.model_dump()                          # → dict
patient.model_dump_json(indent=2)             # → JSON string
patient.model_dump(exclude={"email"})         # exclude a field
patient.model_dump(exclude_none=True)         # skip None fields
Patient.model_validate(raw_dict)              # dict → model
Patient.model_validate_json(json_str)         # JSON → model
```

---

## 🛠️ Improvements Over Original

| Issue in Source | Fix Applied |
|---|---|
| `return v` bug (undefined variable) in `2_field_validator.py` | Fixed to `return value` |
| No `mode="after"` argument in `@model_validator` | Added correctly |
| Missing return type + `Self` hint on model validator | Fixed per Pydantic v2 spec |
| No demos / runnable output | Every file has `print()` demos |
| BMI verdict missing "Overweight" tier | Correct 4-tier WHO classification |
| Flat files with no structure | Sectioned with clear separators |
| Files numbered 1–6 with inconsistent names | Consistent `0N_topic_name.py` naming |

---

## 📄 Reference

- [Pydantic v2 Docs](https://docs.pydantic.dev/latest/)
- [FastAPI + Pydantic](https://fastapi.tiangolo.com/tutorial/body/)
