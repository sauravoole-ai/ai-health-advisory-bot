def validate_health_input(data):
    if data is None:
        return False, "Request body must be valid JSON."

    if "spo2" not in data:
        return False, "SpO2 value is required."

    if "bpm" not in data:
        return False, "BPM value is required."

    spo2 = data.get("spo2")
    bpm = data.get("bpm")

    if not isinstance(spo2, (int, float)):
        return False, "SpO2 must be a number."

    if not isinstance(bpm, (int, float)):
        return False, "BPM must be a number."

    if spo2 < 0 or spo2 > 100:
        return False, "SpO2 must be between 0 and 100."

    if bpm < 0 or bpm > 250:
        return False, "BPM must be between 0 and 250."

    return True, "Valid input."