from flask import Flask, jsonify, request, render_template
from datetime import datetime

from services.vitals_analyzer import analyze_vitals, get_status_details
from services.input_validator import validate_health_input
from services.ai_advisor import generate_ai_advice
from services.chat_advisor import generate_chat_response
from config import GROQ_API_KEY, MODEL_NAME

app = Flask(__name__)

DISCLAIMER = "This is not a medical diagnosis. Please consult a qualified healthcare professional for proper evaluation."

# In-memory storage for latest ESP32 / AIoT reading.
# Good for local demo. Later, database storage can be added.
latest_sensor_result = {
    "available": False,
    "message": "No live sensor data received yet."
}


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "app_name": "AI Health Advisory Assistant",
        "status": "running",
        "ai_model": MODEL_NAME,
        "groq_key_loaded": bool(GROQ_API_KEY),
        "available_endpoints": {
            "home": "GET /",
            "health_check": "GET /api/health",
            "manual_vitals_analysis": "POST /api/analyze-health",
            "live_sensor_data_receive": "POST /api/sensor-data",
            "latest_sensor_data": "GET /api/latest-sensor-data",
            "chat": "POST /api/chat"
        },
        "message": "Backend health check successful"
    })


@app.route("/api/analyze-health", methods=["POST"])
def analyze_health():
    """
    Manual Vitals Analysis Mode.

    User manually enters:
    - SpO2
    - BPM
    - Symptoms

    Backend validates, analyzes using safety rules,
    then AI explains the backend-decided status.
    """

    data = request.get_json()

    is_valid, error_message = validate_health_input(data)

    if not is_valid:
        return jsonify({
            "status": "error",
            "message": error_message,
            "disclaimer": DISCLAIMER
        }), 400

    spo2 = data.get("spo2")
    bpm = data.get("bpm")
    symptoms = data.get("symptoms", "")

    status = analyze_vitals(spo2, bpm, symptoms)
    status_details = get_status_details(status)

    ai_advice = generate_ai_advice(
        spo2=spo2,
        bpm=bpm,
        symptoms=symptoms,
        status=status,
        status_details=status_details
    )

    return jsonify({
        "received_data": {
            "spo2": spo2,
            "bpm": bpm,
            "symptoms": symptoms
        },
        "status": status,
        "risk_level": status_details["risk_level"],
        "status_color": status_details["status_color"],
        "short_advice": status_details["short_advice"],
        "ai_advice": ai_advice,
        "message": "Health data analyzed successfully",
        "disclaimer": DISCLAIMER
    }), 200


@app.route("/api/sensor-data", methods=["POST"])
def receive_sensor_data():
    """
    Live Monitor / AIoT Mode.

    ESP32 will later send JSON like:

    {
        "spo2": 97,
        "bpm": 78,
        "device_id": "ESP32_HEALTH_01"
    }

    Optional:
    {
        "symptoms": "mild weakness"
    }

    This route:
    1. Receives live ESP32 sensor data.
    2. Validates SpO2 and BPM.
    3. Runs backend vitals safety analysis.
    4. Generates AI explanation.
    5. Stores the latest result for frontend Live Monitor.
    """

    global latest_sensor_result

    data = request.get_json()

    if data is None:
        return jsonify({
            "status": "error",
            "message": "Request body must be valid JSON.",
            "disclaimer": DISCLAIMER
        }), 400

    sensor_payload = {
        "spo2": data.get("spo2"),
        "bpm": data.get("bpm"),
        "symptoms": data.get("symptoms", "")
    }

    is_valid, error_message = validate_health_input(sensor_payload)

    if not is_valid:
        return jsonify({
            "status": "error",
            "message": error_message,
            "disclaimer": DISCLAIMER
        }), 400

    spo2 = sensor_payload["spo2"]
    bpm = sensor_payload["bpm"]
    symptoms = sensor_payload["symptoms"]
    device_id = data.get("device_id", "ESP32_HEALTH_01")

    status = analyze_vitals(spo2, bpm, symptoms)
    status_details = get_status_details(status)

    ai_advice = generate_ai_advice(
        spo2=spo2,
        bpm=bpm,
        symptoms=symptoms,
        status=status,
        status_details=status_details
    )

    latest_sensor_result = {
        "available": True,
        "source": "live_sensor",
        "device_id": device_id,
        "received_data": {
            "spo2": spo2,
            "bpm": bpm,
            "symptoms": symptoms
        },
        "status": status,
        "risk_level": status_details["risk_level"],
        "status_color": status_details["status_color"],
        "short_advice": status_details["short_advice"],
        "ai_advice": ai_advice,
        "message": "Live sensor data received and analyzed successfully",
        "disclaimer": DISCLAIMER,
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return jsonify(latest_sensor_result), 200


@app.route("/api/latest-sensor-data", methods=["GET"])
def get_latest_sensor_data():
    """
    Frontend Live Monitor calls this repeatedly.
    Returns the latest ESP32 / AIoT advisory result.
    """

    return jsonify(latest_sensor_result), 200


@app.route("/api/chat", methods=["POST"])
def chat():
    """
    AI Health Chat Mode.

    Supports:
    - typed health chatbot
    - voice chat mode using same backend route
    """

    data = request.get_json()

    if data is None:
        return jsonify({
            "status": "error",
            "reply": "Request body must be valid JSON.",
            "disclaimer": DISCLAIMER
        }), 400

    user_message = data.get("message", "")
    history = data.get("history", [])

    chat_response = generate_chat_response(
        user_message=user_message,
        history=history
    )

    if chat_response["status"] == "error":
        return jsonify(chat_response), 400

    return jsonify(chat_response), 200


if __name__ == "__main__":
    app.run(debug=True)