# FastAPI 

> A clean, well-structured FastAPI project covering **Patient Management** and **Insurance Premium Prediction** with a machine learning model.

---

## 📁 Project Structure

```
FastAPI/
├── main.py            # Patient CRUD API
├── app.py             # Insurance Premium ML Prediction API
├── frontend.py        # Streamlit UI for the prediction API
├── patients.json      # Persistent patient data store
├── insurance.csv      # Dataset used to train the ML model
├── model.pkl          # Trained scikit-learn model
├── requirements.txt   # Python dependencies
└── README.md
```

---

## 🚀 Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Patient Management API

```bash
uvicorn main:app --reload
```

### 3. Run the Insurance Prediction API

```bash
uvicorn app:app --reload --port 8001
```

### 4. Run the Streamlit frontend

> Update `API_URL` in `frontend.py` if needed before running.

```bash
streamlit run frontend.py
```

---

## 📖 API Reference

### Patient Management API (`main.py`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `GET` | `/patients` | List all patients |
| `GET` | `/patients/{id}` | Get a patient by ID |
| `GET` | `/patients/sort/by?sort_by=age&order=asc` | Sort patients |
| `POST` | `/patients` | Create a new patient |
| `PUT` | `/patients/{id}` | Update an existing patient |
| `DELETE` | `/patients/{id}` | Delete a patient |

**Auto-computed fields** (no need to provide): `bmi`, `verdict`

### Insurance Prediction API (`app.py`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `POST` | `/predict` | Predict premium category |

**Auto-computed fields** (no need to provide): `bmi`, `city_tier`, `lifestyle_risk`

---

## ✨ Key Improvements Over Original

| Feature | Original | This Version |
|---------|----------|--------------|
| Error handling | Basic | Proper HTTP status codes (404, 409, 500) |
| Pydantic v2 | Partial | Fully updated (`model_dump`, `computed_field`) |
| BMI verdict | Overweight == Normal (bug) | Correct WHO categories |
| City lookup | List — O(n) | `frozenset` — O(1) |
| Model loading | Silent failure | Fail-fast with clear message |
| Response models | None | `PredictionResponse` schema |
| Documentation | Minimal | Rich docstrings, examples, tags |
| Code style | Flat | Sectioned with clear separators |

---

## 📚 Interactive Docs

Once the server is running, visit:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🛠️ Tech Stack

- **[FastAPI](https://fastapi.tiangolo.com/)** — Modern Python web framework
- **[Pydantic v2](https://docs.pydantic.dev/latest/)** — Data validation & serialisation
- **[Uvicorn](https://www.uvicorn.org/)** — ASGI server
- **[scikit-learn](https://scikit-learn.org/)** — ML model
- **[Streamlit](https://streamlit.io/)** — Frontend UI

---

## 📄 License

MIT — see [LICENSE](LICENSE) for details.
