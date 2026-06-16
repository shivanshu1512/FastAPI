"""
Patient Management API
======================
A professional FastAPI application for managing patient health records.
Supports full CRUD operations with BMI calculation and health verdict.
"""

from fastapi import FastAPI, Path, HTTPException, Query, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json
from pathlib import Path as FilePath

# ─────────────────────────────────────────────
# App Configuration
# ─────────────────────────────────────────────

app = FastAPI(
    title="Patient Management API",
    description=(
        "A professional REST API for managing patient health records. "
        "Supports creating, reading, updating, and deleting patients, "
        "with automatic BMI calculation and health verdict."
    ),
    version="1.0.0",
    contact={
        "name": "Shivanshu Shukla",
        "url": "https://github.com/shivanshu1512",
    },
    license_info={"name": "MIT"},
)

DATA_FILE = FilePath("patients.json")


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def load_data() -> dict:
    """Load patient records from the JSON store."""
    if not DATA_FILE.exists():
        return {}
    with DATA_FILE.open("r") as f:
        return json.load(f)


def save_data(data: dict) -> None:
    """Persist patient records to the JSON store."""
    with DATA_FILE.open("w") as f:
        json.dump(data, f, indent=2)


# ─────────────────────────────────────────────
# Schemas
# ─────────────────────────────────────────────

class Patient(BaseModel):
    """Schema for creating a new patient record."""

    id: Annotated[str, Field(..., description="Unique patient ID", examples=["P001"])]
    name: Annotated[str, Field(..., min_length=2, description="Full name of the patient")]
    city: Annotated[str, Field(..., description="City where the patient resides")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age in years")]
    gender: Annotated[
        Literal["male", "female", "other"],
        Field(..., description="Biological gender"),
    ]
    height: Annotated[float, Field(..., gt=0, description="Height in metres (e.g. 1.75)")]
    weight: Annotated[float, Field(..., gt=0, description="Weight in kilograms")]

    @computed_field  # type: ignore[misc]
    @property
    def bmi(self) -> float:
        """Body Mass Index rounded to 2 decimal places."""
        return round(self.weight / (self.height ** 2), 2)

    @computed_field  # type: ignore[misc]
    @property
    def verdict(self) -> str:
        """WHO weight-status category derived from BMI."""
        if self.bmi < 18.5:
            return "Underweight"
        if self.bmi < 25.0:
            return "Normal"
        if self.bmi < 30.0:
            return "Overweight"
        return "Obese"


class PatientUpdate(BaseModel):
    """Schema for partially updating an existing patient record (all fields optional)."""

    name: Annotated[Optional[str], Field(default=None, min_length=2)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0, lt=120)]
    gender: Annotated[Optional[Literal["male", "female", "other"]], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


# ─────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────

@app.get("/", tags=["Health"])
def root():
    """API health-check endpoint."""
    return {"status": "ok", "message": "Patient Management API is running 🚀"}


@app.get("/patients", tags=["Patients"], summary="List all patients")
def get_all_patients():
    """Return every patient record in the store."""
    return load_data()


@app.get(
    "/patients/{patient_id}",
    tags=["Patients"],
    summary="Get a single patient",
    responses={404: {"description": "Patient not found"}},
)
def get_patient(
    patient_id: Annotated[str, Path(..., description="The patient's unique ID")],
):
    """Retrieve a patient record by their ID."""
    data = load_data()
    if patient_id not in data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient '{patient_id}' not found.",
        )
    return data[patient_id]


@app.get("/patients/sort/by", tags=["Patients"], summary="Sort patients by a field")
def sort_patients(
    sort_by: Annotated[
        Literal["age", "bmi", "name"],
        Query(description="Field to sort by"),
    ] = "age",
    order: Annotated[
        Literal["asc", "desc"],
        Query(description="Sort direction"),
    ] = "asc",
):
    """
    Return all patients sorted by a chosen field.

    - **sort_by**: `age`, `bmi`, or `name`
    - **order**: `asc` (ascending) or `desc` (descending)
    """
    data = load_data()
    reverse = order == "desc"
    try:
        sorted_patients = sorted(data.values(), key=lambda p: p[sort_by], reverse=reverse)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot sort by '{sort_by}'.",
        )
    return sorted_patients


@app.post(
    "/patients",
    tags=["Patients"],
    summary="Create a new patient",
    status_code=status.HTTP_201_CREATED,
    responses={409: {"description": "Patient ID already exists"}},
)
def create_patient(patient: Patient):
    """
    Register a new patient.

    BMI and verdict are **automatically computed** from height and weight —
    you do not need to supply them.
    """
    data = load_data()
    if patient.id in data:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Patient with ID '{patient.id}' already exists.",
        )
    data[patient.id] = patient.model_dump()
    save_data(data)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "Patient created successfully.", "patient": data[patient.id]},
    )


@app.put(
    "/patients/{patient_id}",
    tags=["Patients"],
    summary="Update a patient (partial update supported)",
    responses={404: {"description": "Patient not found"}},
)
def update_patient(
    patient_id: Annotated[str, Path(..., description="The patient's unique ID")],
    updates: PatientUpdate,
):
    """
    Update one or more fields of an existing patient.

    Only the fields you include in the request body will be modified.
    BMI and verdict are **recalculated automatically** after any update.
    """
    data = load_data()
    if patient_id not in data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient '{patient_id}' not found.",
        )

    record = data[patient_id]
    for field, value in updates.model_dump(exclude_none=True).items():
        record[field] = value

    # Recalculate derived fields
    height = record["height"]
    weight = record["weight"]
    bmi = round(weight / (height ** 2), 2)
    record["bmi"] = bmi
    record["verdict"] = (
        "Underweight" if bmi < 18.5
        else "Normal" if bmi < 25
        else "Overweight" if bmi < 30
        else "Obese"
    )

    data[patient_id] = record
    save_data(data)
    return {"message": "Patient updated successfully.", "patient": record}


@app.delete(
    "/patients/{patient_id}",
    tags=["Patients"],
    summary="Delete a patient",
    responses={404: {"description": "Patient not found"}},
)
def delete_patient(
    patient_id: Annotated[str, Path(..., description="The patient's unique ID")],
):
    """Permanently remove a patient record."""
    data = load_data()
    if patient_id not in data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient '{patient_id}' not found.",
        )
    removed = data.pop(patient_id)
    save_data(data)
    return {"message": f"Patient '{patient_id}' deleted.", "patient": removed}
