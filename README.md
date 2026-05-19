# 🩺 AI Health Advisory Assistant

A professional Flask-based **AI healthcare advisory web app** with manual vitals analysis, AI health chatbot, voice interaction, and AIoT-ready live sensor monitoring.

The project is designed for a future **ESP32 + MAX30102** setup where SpO₂ and BPM readings can be sent automatically to the backend, analyzed through safety rules, explained by AI, and shown on the UI with smart voice advisory.

> ⚠️ This project is for educational and preliminary health guidance only. It is not a medical diagnosis system.

---

## 🚀 Project Highlights

- 🫀 Manual SpO₂ and BPM analysis
- 📡 AIoT-ready live sensor monitor
- 🤖 AI-powered health chatbot
- 🎙️ Voice-based AI health chat
- 🔊 Smart live voice advisory for sensor updates
- 🛡️ Rule-based safety engine for vitals
- 🚨 Emergency symptom safety handling
- 💊 Medicine-suggestion safety filtering
- 📄 Copy and Save-as-PDF options
- 📱 Responsive sidebar dashboard UI
- ⚙️ ESP32/MAX30102 backend API support

---

## 🧠 Main Modes

### 1. 🫀 Vitals Analysis Mode

#### Manual Entry

Users can manually enter:

- SpO₂ level
- Heart rate / BPM
- Symptoms or health concern

The backend validates the input, analyzes it using rule-based safety logic, and generates simple AI-assisted advice.

#### Live Monitor / AIoT Mode

This mode is prepared for automatic sensor-based monitoring.

Expected final flow:

```text
MAX30102 Sensor → ESP32 → Flask Backend → Safety Analysis → AI Advisory → UI + Voice Output

The backend already includes API support for receiving live ESP32 sensor data.

2. 🤖 AI Health Chat Mode

A typed health chatbot for preliminary health-related questions.

It supports:

Symptom-related guidance
Follow-up questions
Practical precautions
Emergency safety redirection
Out-of-scope query handling
Medical disclaimer
3. 🎙️ AI Voice Chat Mode

A voice-enabled mode where users can speak health-related questions and receive spoken AI replies.

Features:

Speak Once mode
Auto conversation mode
Speech-to-text input
Text-to-speech AI response
Works best in Google Chrome
🛡️ Safety Architecture

This project follows a safety-first design.

Vitals Safety

The backend decides the vitals status using rule-based logic.

The AI does not independently decide the emergency level for vitals. It only explains the backend-decided result in simple language.

Chatbot Safety

The chatbot includes handling for:

Emergency symptoms
Medicine-related responses
Out-of-scope questions
Identity questions
Numeric-only unclear input
Missing or vague context

Every response includes a medical disclaimer.

🧰 Tech Stack
Backend
Python
Flask
Groq API
python-dotenv
Frontend
HTML
CSS
JavaScript
Browser Speech Recognition API
Browser Text-to-Speech API
AI Model
Groq API
llama-3.1-8b-instant
AIoT Hardware Ready
ESP32
MAX30102 pulse oximeter sensor
0.96 inch OLED display
Breadboard
Jumper wires
📁 Project Structure
ai-health-advisory-bot/
│
├── README.md
│
└── backend/
    ├── app.py
    ├── config.py
    ├── requirements.txt
    ├── .env.example
    ├── .gitignore
    ├── test_cases.md
    │
    ├── services/
    │   ├── ai_advisor.py
    │   ├── chat_advisor.py
    │   ├── input_validator.py
    │   └── vitals_analyzer.py
    │
    ├── templates/
    │   └── index.html
    │
    ├── static/
    │   ├── css/
    │   │   └── style.css
    │   └── js/
    │       ├── script.js
    │       └── voice.js
    │
    └── venv/
🔐 Environment Variables

Create a .env file inside the backend/ folder:

GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=llama-3.1-8b-instant

Use .env.example as reference:

GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=llama-3.1-8b-instant

Never upload the real .env file to GitHub.

⚙️ Installation & Setup
1. Clone the repository
git clone https://github.com/your-username/ai-health-advisory-bot.git
cd ai-health-advisory-bot/backend
2. Create virtual environment
python -m venv venv
3. Activate virtual environment

For Windows CMD:

venv\Scripts\activate

For Windows PowerShell:

.\venv\Scripts\Activate.ps1
4. Install dependencies
pip install -r requirements.txt
5. Add .env

Create this file:

backend/.env

Add:

GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=llama-3.1-8b-instant
6. Run the app
python app.py

Open in browser:

http://127.0.0.1:5000
🔌 API Endpoints
Health Check
GET /api/health
Manual Health Analysis
POST /api/analyze-health

Example:

{
  "spo2": 97,
  "bpm": 78,
  "symptoms": "mild tiredness"
}
Live Sensor Data
POST /api/sensor-data

Example ESP32 payload:

{
  "spo2": 97,
  "bpm": 78,
  "device_id": "ESP32_HEALTH_01"
}

Emergency-style payload:

{
  "spo2": 88,
  "bpm": 118,
  "symptoms": "severe breathlessness",
  "device_id": "ESP32_HEALTH_01"
}
Latest Sensor Data
GET /api/latest-sensor-data
AI Health Chat
POST /api/chat

Example:

{
  "message": "I feel weak and tired. What should I do?",
  "history": []
}
📡 Live AIoT Monitor Behavior

The Live Monitor mode automatically fetches the latest sensor result from the backend.

Smart voice advisory rules:

Normal reading: speaks once
Caution reading: speaks on meaningful updates
Emergency reading: speaks urgent updates
Status change: always speaks
Manual mode: no automatic voice

This keeps the demo realistic without repeated unnecessary speech.

🧪 Example Test Inputs
Normal Reading
{
  "spo2": 97,
  "bpm": 78,
  "device_id": "ESP32_HEALTH_01"
}
Caution Reading
{
  "spo2": 93,
  "bpm": 92,
  "device_id": "ESP32_HEALTH_01"
}
Emergency Reading
{
  "spo2": 88,
  "bpm": 118,
  "symptoms": "severe breathlessness",
  "device_id": "ESP32_HEALTH_01"
}
🧾 Disclaimer

This application does not provide medical diagnosis, prescription, or treatment.

It is only a preliminary health advisory tool for educational and demonstration purposes.

For serious, persistent, or worsening symptoms, consult a qualified healthcare professional immediately.

For emergency symptoms such as chest pain, severe breathlessness, fainting, confusion, blue lips, or very low SpO₂, seek urgent medical help.

🔮 Future Hardware Integration

The software is already prepared for ESP32-based sensor integration.

Planned hardware flow:

MAX30102 reads SpO₂ and BPM
ESP32 receives sensor values
ESP32 sends JSON data to Flask backend using Wi-Fi
Backend analyzes readings
AI explains the result
UI updates automatically
Voice advisory speaks important updates

🎯 Resume Highlight

Built a Flask-based AI Health Advisory Assistant with manual vitals analysis, AI chatbot, voice interaction, and AIoT-ready ESP32 sensor data integration using Groq API and rule-based medical safety checks.