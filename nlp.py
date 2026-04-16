def nlp_risk(text):
    text = text.lower()
    risk = 0

    if "stress" in text or "tension" in text:
        risk += 15
    if "tired" in text or "no sleep" in text:
        risk += 10
    if "smoking" in text:
        risk += 15

    return risk