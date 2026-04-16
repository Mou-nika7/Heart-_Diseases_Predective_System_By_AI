import streamlit as st
import pandas as pd

from utils import calculate_risk, apply_age_multiplier, classify_simple, generate_suggestions
from nlp import nlp_risk
from model import train_models, predict_models

st.set_page_config(page_title="Heart Health AI", layout="wide")

# -------- FULL DARK 3D UI STYLE --------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}

/* Cards */
.section {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(12px);
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 20px;
    box-shadow: 0px 8px 30px rgba(0,0,0,0.4);
}

/* Titles */
.title {
    font-size: 22px;
    font-weight: bold;
    margin-bottom: 10px;
}

/* Risk Colors */
.risk-low {color: #00ffcc; font-size:24px; font-weight:bold;}
.risk-medium {color: #ffcc00; font-size:24px; font-weight:bold;}
.risk-high {color: #ff4d4d; font-size:24px; font-weight:bold;}

/* Suggestions */
.suggestion {
    background: rgba(255,255,255,0.1);
    padding: 12px;
    border-radius: 10px;
    margin: 5px 0;
    border-left: 4px solid #00c6ff;
}

/* Button */
.stButton>button {
    background: linear-gradient(45deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 10px;
    height: 45px;
    font-size: 16px;
    border: none;
}

/* Labels white */
label {color: white !important;}
h1 {text-align: center;}

</style>
""", unsafe_allow_html=True)

st.title("💖 Heart Health Risk AI Assistant")

# -------- INPUT SECTION --------
st.markdown('<div class="section">', unsafe_allow_html=True)
st.markdown('<div class="title">Input Details</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    age = st.slider("Age", 10, 100)
    gender = st.selectbox("Gender", ["Male", "Female"])

    smoke_choice = st.radio("Do you smoke?", ["No", "Yes"])
    smoking = st.slider("Cigarettes per day", 1, 20) if smoke_choice == "Yes" else 0

    alcohol_choice = st.radio("Do you drink alcohol?", ["No", "Yes"])
    alcohol = st.slider("Drinks per day", 1, 10) if alcohol_choice == "Yes" else 0

    stress = st.selectbox("Stress Level", ["Low", "Medium", "High"])
    sleep = st.slider("Sleep hours", 1, 10)

with col2:
    activity = st.selectbox("Physical Activity", ["Low", "Medium", "High"])
    pollution = st.selectbox("Pollution Exposure", ["Low", "High"])

    bp = st.number_input("Blood Pressure", min_value=50, max_value=200, step=1)
    chol = st.number_input("Cholesterol", min_value=50, max_value=400, step=1)
    sugar = st.number_input("Sugar", min_value=50, max_value=300, step=1)

    ecg = st.selectbox("ECG", ["Normal", "Abnormal"])
    angina = st.selectbox("Angina", ["No", "Yes"])

text = st.text_area("Describe your health")

st.markdown('</div>', unsafe_allow_html=True)

# -------- LOAD MODELS --------
@st.cache_resource
def load_models():
    return train_models()

rf, dl = load_models()

# -------- PREDICT --------
if st.button("Predict Risk"):

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

    level = classify_simple(final)

    # -------- RISK --------
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="title">Risk Level</div>', unsafe_allow_html=True)

    if level == "LOW":
        st.markdown(f"<div class='risk-low'>LOW ({round(final,1)}%)</div>", unsafe_allow_html=True)
    elif level == "MODERATE":
        st.markdown(f"<div class='risk-medium'>MODERATE ({round(final,1)}%)</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='risk-high'>HIGH ({round(final,1)}%)</div>", unsafe_allow_html=True)

    st.progress(int(final))
    st.markdown('</div>', unsafe_allow_html=True)

    # -------- PREDICTIONS --------
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="title">Predictions</div>', unsafe_allow_html=True)

    features = pd.DataFrame(
        [[age, smoking, alcohol, sleep, bp, chol, sugar]],
        columns=["age","smoking","alcohol","sleep","bp","cholesterol","sugar"]
    )

    rf_pred, dl_pred = predict_models(rf, dl, features)

    ml_percent = 100 if rf_pred == 1 else 0
    dl_percent = int(dl_pred * 100)

    st.write("ML Model")
    st.progress(ml_percent)

    st.write("DL Model")
    st.progress(dl_percent)

    st.markdown('</div>', unsafe_allow_html=True)

    # -------- SUGGESTIONS --------
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="title">Suggestions</div>', unsafe_allow_html=True)

    suggestions = generate_suggestions(data, final)

    for s in suggestions:
        if s.strip() != "":
            st.markdown(f"<div class='suggestion'>{s}</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)