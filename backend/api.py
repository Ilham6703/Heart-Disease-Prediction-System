from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import pandas as pd
import joblib
import traceback

# =========================
# Load Artifacts
# =========================

model = joblib.load("KNN_heart.pkl")
scaler = joblib.load("scaler.pkl")
columns = joblib.load("columns.pkl")

# =========================
# FastAPI App
# =========================

app = FastAPI(
    title="Heart Disease Prediction API",
    description="Machine Learning API for Heart Disease Risk Prediction",
    version="1.0.0"
)

# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # We'll restrict this later when deployed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Input Schema
# =========================

class HeartData(BaseModel):

    Age: int = Field(..., ge=1, le=120)

    RestingBP: float = Field(..., ge=50, le=300)

    Cholesterol: float = Field(..., ge=0, le=1000)

    FastingBS: int = Field(..., ge=0, le=1)

    MaxHR: float = Field(..., ge=50, le=300)

    Oldpeak: float = Field(..., ge=0, le=10)

    Sex: str

    ChestPainType: str

    RestingECG: str

    ExerciseAngina: str

    ST_Slope: str


# =========================
# Routes
# =========================

@app.get("/")
def home():

    return {
        "message": "Heart Disease Prediction API Running Successfully"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.post("/predict")
def predict(data: HeartData):

    try:

        input_data = {
            'Age': data.Age,
            'RestingBP': data.RestingBP,
            'Cholesterol': data.Cholesterol,
            'FastingBS': data.FastingBS,
            'MaxHR': data.MaxHR,
            'Oldpeak': data.Oldpeak,

            'Sex_M': 1 if data.Sex == "M" else 0,

            'ChestPainType_ATA': 1 if data.ChestPainType == "ATA" else 0,
            'ChestPainType_NAP': 1 if data.ChestPainType == "NAP" else 0,
            'ChestPainType_TA': 1 if data.ChestPainType == "TA" else 0,

            'RestingECG_Normal': 1 if data.RestingECG == "Normal" else 0,
            'RestingECG_ST': 1 if data.RestingECG == "ST" else 0,

            'ExerciseAngina_Y': 1 if data.ExerciseAngina == "Y" else 0,

            'ST_Slope_Flat': 1 if data.ST_Slope == "Flat" else 0,
            'ST_Slope_Up': 1 if data.ST_Slope == "Up" else 0
        }

        df = pd.DataFrame([input_data])

        df = df.reindex(
            columns=columns,
            fill_value=0
        )

        scaled_data = scaler.transform(df)

        prediction = int(
            model.predict(scaled_data)[0]
        )

        probabilities = model.predict_proba(
            scaled_data
        )[0]

        confidence = round(
            max(probabilities) * 100,
            2
        )

        risk_level = (
            "High Risk"
            if prediction == 1
            else "Low Risk"
        )

        return {
            "success": True,
            "prediction": prediction,
            "risk_level": risk_level,
            "confidence": confidence
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e),
            "trace": traceback.format_exc()
        }