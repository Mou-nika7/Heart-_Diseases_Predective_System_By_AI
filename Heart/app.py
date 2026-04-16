import streamlit as st
import pandas as pd

from utils import calculate_risk, apply_age_multiplier, classify_risk
from nlp import nlp_risk
from model import train_models, predict_models

st.set_page_config(page_title="Heart Health AI", layout="wide")

# -------- UI STYLE --------
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(to right, #ff9a9e, #a18cd1, #89f7fe);
    }
    .card {
        background: rgba(255,255,255,0.2);
        padding: 20px;
        border-radius: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("💖 Heart Health Risk AI Assistant")

# -------- INPUTS --------
age = st.slider("Age", 10, 100)
gender = st.selectbox("Gender", ["Male", "Female"])
smoking = st.slider("Smoking per day", 0, 20)
alcohol = st.slider("Alcohol per day", 0, 10)
stress = st.selectbox("Stress", ["Low", "Medium", "High"])
sleep = st.slider("Sleep hours", 1, 10)
activity = st.selectbox("Physical Activity", ["Low", "Medium", "High"])
pollution = st.selectbox("Pollution", ["Low", "High"])

bp = st.number_input("Blood Pressure", 80, 200)
chol = st.number_input("Cholesterol", 100, 400)
sugar = st.number_input("Sugar", 70, 200)
ecg = st.selectbox("ECG", ["Normal", "Abnormal"])
angina = st.selectbox("Angina", ["No", "Yes"])

text = st.text_area("Describe your health")

# -------- LOAD MODEL (OPTIMIZED) --------
@st.cache_resource
def load_models():
    return train_models()

rf, dl = load_models()

# -------- PREDICTION --------
if st.button("Predict"):

    data = {
        "age": age,
        "gender": gender,
        "smoking": smoking,
        "alcohol": alcohol,
        "stress": stress,
        "sleep": sleep,
        "activity": activity,
        "pollution": pollution,
        "bp": bp,
        "cholesterol": chol,
        "sugar": sugar,
        "ecg": ecg,
        "angina": angina
    }

    base = calculate_risk(data)
    nlp_score = nlp_risk(text)

    total = base + nlp_score
    final = apply_age_multiplier(age, total)

    category = classify_risk(final)

    st.subheader(f"Final Risk Score: {round(final,2)}")
    st.success(f"Risk Level: {category}")

    # -------- ML + DL --------
    features = pd.DataFrame(
        [[age, smoking, alcohol, sleep, bp, chol, sugar]],
        columns=["age","smoking","alcohol","sleep","bp","cholesterol","sugar"]
    )

    rf_pred, dl_pred = predict_models(rf, dl, features)

    st.write("ML Prediction:", rf_pred)
    st.write("DL Prediction:", round(dl_pred, 2))

    # -------- UI --------
    st.progress(int(final))
    st.balloons()