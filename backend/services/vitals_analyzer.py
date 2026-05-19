def analyze_vitals(spo2, bpm, symptoms):
    symptoms_lower = symptoms.lower()

    emergency_keywords = [
        "chest pain",
        "severe breathlessness",
        "unconsciousness",
        "bluish lips",
        "confusion"
    ]

    for keyword in emergency_keywords:
        if keyword in symptoms_lower:
            return "Emergency Attention"

    if spo2 < 90 or bpm < 40 or bpm > 130:
        return "Emergency Attention"

    if spo2 < 95 or bpm < 50 or bpm > 120:
        return "High Caution"

    if bpm < 60 or bpm > 100:
        return "Mild Caution"

    return "Normal"


def get_status_details(status):
    if status == "Normal":
        return {
            "risk_level": 1,
            "status_color": "green",
            "short_advice": "Your readings look generally normal. Continue healthy habits and monitor if symptoms increase."
        }

    if status == "Mild Caution":
        return {
            "risk_level": 2,
            "status_color": "yellow",
            "short_advice": "There is a mild variation in your readings. Rest, hydrate, and observe your condition."
        }

    if status == "High Caution":
        return {
            "risk_level": 3,
            "status_color": "orange",
            "short_advice": "Your readings need attention. Monitor closely and consider consulting a healthcare professional."
        }

    return {
        "risk_level": 4,
        "status_color": "red",
        "short_advice": "Your readings or symptoms may need urgent attention. Please seek immediate medical help."
    }