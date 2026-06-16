"""
Insurance Premium Predictor API
================================
A production-ready FastAPI application that serves an ML model
to predict health insurance premium categories.
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import pickle
import pandas as pd
from pathlib import Path

# ─────────────────────────────────────────────
# Load ML Model (fail fast at startup)
# ─────────────────────────────────────────────

MODEL_PATH = Path("model.pkl")

try:
    with MODEL_PATH.open("rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    raise RuntimeError(
        f"Model file not found at '{MODEL_PATH}'. "
        "Please train and export the model before starting the API."
    )

# ─────────────────────────────────────────────
# City-tier lookup
# ─────────────────────────────────────────────

TIER_1_CITIES: frozenset[str] = frozenset({
    "Mumbai", "Delhi", "Bangalore", "Chennai",
    "Kolkata", "Hyderabad", "Pune",
})

TIER_2_CITIES: frozenset[str] = frozenset({
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi",
    "Visakhapatnam", "Coimbatore", "Bhopal", "Nagpur", "Vadodara",
    "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati",
    "Thiruvananthapuram", "Ludhiana", "Nashik", "Allahabad", "Udaipur",
    "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada",
    "Tiruchirappalli", "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly",
    "Aligarh", "Gaya", "Kozhikode", "Warangal", "Kolhapur", "Bilaspur",
    "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri",
})


def get_city_tier(city: str) -> str:
    """Return the tier label for a given Indian city."""
    if city in TIER_1_CITIES:
        return "Tier 1"
    if city in TIER_2_CITIES:
        return "Tier 2"
    return "Tier 3"


# ─────────────────────────────────────────────
# App Configuration
# ─────────────────────────────────────────────

app = FastAPI(
    title="Insurance Premium Predictor API",
    description=(
        "Submit personal health and demographic data to receive an instant "
        "prediction of your insurance premium category using a trained ML model."
    ),
    version="1.0.0",
    contact={
        "name": "Shivanshu Shukla",
        "url": "https://github.com/shivanshu1512",
    },
    license_info={"name": "MIT"},
)


# ─────────────────────────────────────────────
# Schemas
# ─────────────────────────────────────────────

class PredictionRequest(BaseModel):
    """Input schema for the /predict endpoint."""

    age: Annotated[int, Field(..., gt=0, lt=120, description="Age in years", examples=[30])]
    weight: Annotated[float, Field(..., gt=0, description="Weight in kg", examples=[70.0])]
    height: Annotated[float, Field(..., gt=0, description="Height in metres", examples=[1.75])]
    income_lpa: Annotated[
        float,
        Field(..., gt=0, description="Annual income in Lakhs Per Annum", examples=[10.0]),
    ]
    smoker: Annotated[bool, Field(..., description="Whether the applicant is a smoker")]
    city: Annotated[str, Field(..., description="City of residence", examples=["Mumbai"])]
    occupation: Annotated[
        Literal[
            "retired", "freelancer", "student",
            "government_job", "business_owner",
            "unemployed", "private_job",
        ],
        Field(..., description="Current occupation"),
    ]

    @computed_field  # type: ignore[misc]
    @property
    def bmi(self) -> float:
        """Derived BMI from height and weight."""
        return round(self.weight / (self.height ** 2), 2)

    @computed_field  # type: ignore[misc]
    @property
    def lifestyle_risk(self) -> str:
        """Simple lifestyle risk indicator."""
        if self.smoker and self.bmi >= 30:
            return "high"
        if self.smoker or self.bmi >= 30:
            return "medium"
        return "low"

    @computed_field  # type: ignore[misc]
    @property
    def city_tier(self) -> str:
        """City tier classification (Tier 1 / 2 / 3)."""
        return get_city_tier(self.city)


class PredictionResponse(BaseModel):
    """Response schema returned by the /predict endpoint."""

    prediction: str = Field(..., description="Predicted premium category")
    bmi: float
    city_tier: str
    lifestyle_risk: str


# ─────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────

@app.get("/", tags=["Health"])
def root():
    """API health-check endpoint."""
    return {"status": "ok", "message": "Insurance Premium Predictor API is running 🚀"}


@app.post(
    "/predict",
    tags=["Prediction"],
    summary="Predict insurance premium category",
    response_model=PredictionResponse,
    responses={422: {"description": "Validation error"}, 500: {"description": "Model inference error"}},
)
def predict(request: PredictionRequest):
    """
    Predict the insurance premium category for an applicant.

    **Computed fields** (auto-derived, do not pass these):
    - `bmi` — calculated from `height` and `weight`
    - `city_tier` — derived from `city`
    - `lifestyle_risk` — derived from `smoker` and `bmi`

    **Returns:** one of `Low`, `Medium`, or `High` premium categories.
    """
    # Build the feature dataframe expected by the model
    features = pd.DataFrame([{
        "age": request.age,
        "weight": request.weight,
        "bmi": request.bmi,
        "income_lpa": request.income_lpa,
        "smoker": request.smoker,
        "city_tier": request.city_tier,
        "occupation": request.occupation,
        "lifestyle_risk": request.lifestyle_risk,
    }])

    try:
        prediction = model.predict(features)[0]
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Model inference failed: {exc}",
        )

    return PredictionResponse(
        prediction=str(prediction),
        bmi=request.bmi,
        city_tier=request.city_tier,
        lifestyle_risk=request.lifestyle_risk,
    )
