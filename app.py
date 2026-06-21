


import streamlit as st
import pandas as pd
import joblib

# Load model and artifacts
model = joblib.load("KNN_heart.pkl")
scaler = joblib.load("scaler.pkl")
columns = joblib.load("columns.pkl")


st.set_page_config(
    page_title="Heart Disease Predictor",
    page_icon="❤️"
)

st.title("❤️ Heart Disease Prediction System")
st.write("Enter patient details and click Predict")

# Numerical Inputs
age = st.number_input("Age", min_value=1, max_value=120, value=40)

resting_bp = st.number_input(
    "Resting Blood Pressure",
    min_value=50,
    max_value=250,
    value=120
)

cholesterol = st.number_input(
    "Cholesterol",
    min_value=50,
    max_value=700,
    value=200
)

fasting_bs = st.selectbox(
    "Fasting Blood Sugar > 120 mg/dl",
    [0, 1]
)

max_hr = st.number_input(
    "Maximum Heart Rate",
    min_value=50,
    max_value=250,
    value=150
)

oldpeak = st.number_input(
    "Old Peak",
    min_value=0.0,
    max_value=10.0,
    value=1.0
)

# Categorical Inputs
sex = st.selectbox(
    "Sex",
    ["M", "F"]
)

chest_pain = st.selectbox(
    "Chest Pain Type",
    ["ATA", "NAP", "TA", "ASY"]
)

resting_ecg = st.selectbox(
    "Resting ECG",
    ["Normal", "ST", "LVH"]
)

exercise_angina = st.selectbox(
    "Exercise Angina",
    ["Y", "N"]
)

st_slope = st.selectbox(
    "ST Slope",
    ["Flat", "Up", "Down"]
)

# Predict Button
if st.button("Predict"):

    input_data = {
        'Age': age,
        'RestingBP': resting_bp,
        'Cholesterol': cholesterol,
        'FastingBS': fasting_bs,
        'MaxHR': max_hr,
        'Oldpeak': oldpeak,

        'Sex_M': 1 if sex == "M" else 0,

        'ChestPainType_ATA': 1 if chest_pain == "ATA" else 0,
        'ChestPainType_NAP': 1 if chest_pain == "NAP" else 0,
        'ChestPainType_TA': 1 if chest_pain == "TA" else 0,

        'RestingECG_Normal': 1 if resting_ecg == "Normal" else 0,
        'RestingECG_ST': 1 if resting_ecg == "ST" else 0,

        'ExerciseAngina_Y': 1 if exercise_angina == "Y" else 0,

        'ST_Slope_Flat': 1 if st_slope == "Flat" else 0,
        'ST_Slope_Up': 1 if st_slope == "Up" else 0,
    }

    input_df = pd.DataFrame([input_data])

    # Ensure exact column order
    input_df = input_df.reindex(
        columns=columns,
        fill_value=0
    )

    input_scaled = scaler.transform(input_df)

    prediction = model.predict(input_scaled)[0]

    probability = model.predict_proba(input_scaled)[0]

    if prediction == 1:
        st.error(
            f"⚠️ Heart Disease Detected\n\nConfidence: {probability[1]*100:.2f}%"
        )
    else:
        st.success(
            f"✅ No Heart Disease Detected\n\nConfidence: {probability[0]*100:.2f}%"
        )