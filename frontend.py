"""
Insurance Premium Predictor — Streamlit Frontend
=================================================
A clean, user-friendly Streamlit UI that calls the FastAPI /predict endpoint.
"""

import streamlit as st
import requests

# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────

API_URL = "http://localhost:8000/predict"  # Change to your deployed URL

st.set_page_config(
    page_title="Insurance Premium Predictor",
    page_icon="🏥",
    layout="centered",
)

# ─────────────────────────────────────────────
# UI
# ─────────────────────────────────────────────

st.title("🏥 Insurance Premium Predictor")
st.markdown(
    "Fill in your details below and click **Predict** to find out your estimated "
    "insurance premium category."
)
st.divider()

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", min_value=1, max_value=119, value=30)
    weight = st.number_input("Weight (kg)", min_value=1.0, value=70.0, step=0.5)
    height = st.number_input("Height (m)", min_value=0.5, max_value=2.5, value=1.75, step=0.01)
    income_lpa = st.number_input("Annual Income (LPA)", min_value=0.1, value=10.0, step=0.5)

with col2:
    city = st.text_input("City", value="Mumbai", placeholder="e.g. Mumbai, Delhi…")
    smoker = st.selectbox("Smoker?", options=["No", "Yes"])
    occupation = st.selectbox(
        "Occupation",
        options=[
            "private_job",
            "government_job",
            "business_owner",
            "freelancer",
            "student",
            "retired",
            "unemployed",
        ],
        format_func=lambda x: x.replace("_", " ").title(),
    )

st.divider()

# ─────────────────────────────────────────────
# Prediction
# ─────────────────────────────────────────────

if st.button("🔍 Predict Premium Category", use_container_width=True, type="primary"):
    payload = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker == "Yes",
        "city": city.strip(),
        "occupation": occupation,
    }

    with st.spinner("Sending request to API…"):
        try:
            response = requests.post(API_URL, json=payload, timeout=10)
            response.raise_for_status()
            result = response.json()

            st.success("✅ Prediction complete!")

            # Display results in metric cards
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Premium Category", result["prediction"])
            m2.metric("BMI", result["bmi"])
            m3.metric("City Tier", result["city_tier"])
            m4.metric("Lifestyle Risk", result["lifestyle_risk"].capitalize())

        except requests.exceptions.ConnectionError:
            st.error(
                "❌ Could not connect to the API. "
                "Make sure the FastAPI server is running at: `" + API_URL + "`"
            )
        except requests.exceptions.HTTPError as exc:
            try:
                detail = exc.response.json().get("detail", str(exc))
            except Exception:
                detail = str(exc)
            st.error(f"❌ API error: {detail}")
        except Exception as exc:
            st.error(f"❌ Unexpected error: {exc}")

st.markdown(
    "<small style='color:grey'>Powered by FastAPI + scikit-learn</small>",
    unsafe_allow_html=True,
)
