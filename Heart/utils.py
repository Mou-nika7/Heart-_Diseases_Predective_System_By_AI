def calculate_risk(data):
    base_risk = 0

    # --- Lifestyle ---
    smoking_risk = 20 + (data["smoking"] * 2) if data["smoking"] > 0 else 0
    alcohol_risk = 15 + (data["alcohol"] * 2) if data["alcohol"] > 0 else 0

    stress_risk = {"Low": 0, "Medium": 10, "High": 20}[data["stress"]]
    sleep_risk = 15 if data["sleep"] < 6 else 0
    activity_risk = 15 if data["activity"] == "Low" else 0
    pollution_risk = 10 if data["pollution"] == "High" else 0

    # --- Medical ---
    medical_risk = 0
    if data["bp"] > 140: medical_risk += 10
    if data["cholesterol"] > 240: medical_risk += 10
    if data["sugar"] > 120: medical_risk += 10
    if data["ecg"] == "Abnormal": medical_risk += 10
    if data["angina"] == "Yes": medical_risk += 10

    # --- Gender Weights ---
    if data["gender"] == "Male":
        weights = {"smoking": 1.1, "alcohol": 1.05, "stress": 1.0, "sleep": 1.0}
    else:
        weights = {"smoking": 1.0, "alcohol": 1.0, "stress": 1.1, "sleep": 1.1}

    # --- Apply Weighting ---
    base_risk = (
        smoking_risk * weights["smoking"] +
        alcohol_risk * weights["alcohol"] +
        stress_risk * weights["stress"] +
        sleep_risk * weights["sleep"] +
        activity_risk +
        pollution_risk +
        medical_risk
    )

    return base_risk


def apply_age_multiplier(age, risk):
    if age <= 20:
        multiplier = 0.8
    elif age <= 30:
        multiplier = 1.0
    elif age <= 50:
        multiplier = 1.2
    elif age <= 70:
        multiplier = 1.5
    else:
        multiplier = 1.8

    final_risk = risk * multiplier
    return min(final_risk, 100)


def classify_risk(score):
    if score <= 25:
        return "OK 🟢"
    elif score <= 50:
        return "Little Risk 🟡"
    elif score <= 75:
        return "Moderate Risk 🟠"
    elif score <= 90:
        return "High Risk 🔴"
    else:
        return "Danger Zone 🚨"