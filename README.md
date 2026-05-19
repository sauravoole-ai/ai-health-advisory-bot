# 🩺 AI Health Advisory Assistant

<p align="center">
  <b>AI-powered health advisory web app with vitals analysis, chatbot support, voice interaction, and AIoT-ready sensor monitoring.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Backend-Flask-2f3e46?style=for-the-badge" />
  <img src="https://img.shields.io/badge/AI-Groq_API-83c5be?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Voice-Enabled-a5d6c8?style=for-the-badge" />
  <img src="https://img.shields.io/badge/AIoT-ESP32_Ready-d8bd7a?style=for-the-badge" />
</p>

---

## ✨ Overview

**AI Health Advisory Assistant** is a Flask-based healthcare AI application that provides preliminary health guidance using:

- Manual SpO₂ and BPM analysis
- AI health chatbot
- Voice-based health interaction
- AIoT-ready live monitor for ESP32 + MAX30102 sensor readings
- Rule-based safety checks before AI explanation

> ⚠️ This project is for educational and preliminary advisory purposes only. It is **not** a medical diagnosis, prescription, or treatment system.

---

## 🚀 Key Features

| Feature | Description |
|---|---|
| 🫀 Manual Vitals Analysis | Analyze SpO₂, BPM, and symptoms manually |
| 📡 Live AIoT Monitor | Ready to receive ESP32/MAX30102 sensor readings |
| 🤖 AI Health Chatbot | Answers basic health-related questions safely |
| 🎙️ AI Voice Chat | Speak health queries and hear AI replies |
| 🔊 Smart Sensor Voice | Speaks meaningful live sensor updates |
| 🛡️ Safety Engine | Backend decides vitals risk before AI explanation |
| 🚨 Emergency Handling | Serious symptoms trigger safety guidance |
| 📄 Export Options | Copy responses and save via browser PDF |
| 📱 Responsive UI | Sidebar dashboard layout for desktop and mobile |

---

## 🧠 Application Modes

### 1. Vitals Analysis

**Manual Entry**

User enters:

- SpO₂
- BPM
- Symptoms

The backend validates the input, analyzes it using rule-based logic, and AI explains the result.

**Live Monitor / AIoT Mode**

Prepared for automatic ESP32 sensor readings.

```text
MAX30102 Sensor → ESP32 → Flask Backend → Safety Engine → AI Advisory → UI + Voice
```

---

### 2. AI Health Chat

Typed chatbot for preliminary health-related questions.

Handles:

- Symptom guidance
- Follow-up questions
- Emergency redirection
- Out-of-scope queries
- Numeric ambiguity
- Medical disclaimer

---

### 3. AI Voice Chat

Voice-based mode using browser speech APIs.

Supports:

- Speak Once mode
- Auto conversation mode
- Speech-to-text input
- Text-to-speech response

> Best tested in Google Chrome.

---

## 🛡️ Safety Architecture

The system separates **risk decision** from **AI explanation**.

```text
Vitals Input / Sensor Data
        ↓
Backend Rule-Based Analysis
        ↓
Status Decided Safely
        ↓
AI Explains the Decided Result
```

The AI does **not** independently decide emergency level for vitals.

Every health response includes a medical disclaimer.

---

## 🧰 Tech Stack

| Layer | Tools |
|---|---|
| Backend | Python, Flask |
| AI | Groq API, Llama 3.1 8B Instant |
| Frontend | HTML, CSS, JavaScript |
| Voice | Browser Speech Recognition + Text-to-Speech |
| AIoT Ready | ESP32, MAX30102, OLED Display |
| Config | python-dotenv |

---

## 📁 Project Structure

```text
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
    └── static/
        ├── css/
        │   └── style.css
        └── js/
            ├── script.js
            └── voice.js
```

---

## ⚙️ Setup

```bash
git clone https://github.com/sauravoole-ai/ai-health-advisory-bot.git
cd ai-health-advisory-bot/backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

Create a `.env` file inside `backend/`:

```env
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=llama-3.1-8b-instant
```

> Never upload the real `.env` file to GitHub.

---

## 🔌 Main API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/health` | GET | Backend health check |
| `/api/analyze-health` | POST | Manual vitals analysis |
| `/api/chat` | POST | AI health chatbot |
| `/api/sensor-data` | POST | Receive ESP32 sensor readings |
| `/api/latest-sensor-data` | GET | Fetch latest sensor result |

Example sensor payload:

```json
{
  "spo2": 97,
  "bpm": 78,
  "device_id": "ESP32_HEALTH_01"
}
```

---

## 🔊 Smart Live Voice Logic

| Reading Type | Voice Behavior |
|---|---|
| Normal | Speaks once |
| Caution | Speaks on meaningful updates |
| Emergency | Speaks urgent advisory |
| Status Change | Always speaks |
| Manual Mode | No automatic voice |

---

## 🧪 Testing

Tested scenarios are listed in:

```text
backend/test_cases.md
```

Includes:

- Manual vitals normal/caution/emergency tests
- Missing input validation
- AI chatbot safety tests
- Out-of-scope query handling
- Copy, clear, and PDF checks
- Basic responsive UI check

---

## 📡 Hardware Status

| Component | Status |
|---|---|
| Backend ESP32 API | Ready |
| Live Monitor UI | Ready |
| ESP32 + MAX30102 real test | Pending |
| OLED display integration | Pending |

Planned flow:

```text
MAX30102 → ESP32 → Flask Backend → AI Advisory → UI + Voice
```

---

## 🧾 Disclaimer

This application does **not** provide medical diagnosis, prescription, or treatment.

For serious, persistent, or worsening symptoms, consult a qualified healthcare professional.  
For emergency symptoms such as chest pain, severe breathlessness, fainting, confusion, blue lips, or very low SpO₂, seek urgent medical help.

---

## 🎯 Resume Highlight

Built a Flask-based **AI Health Advisory Assistant** with manual vitals analysis, AI chatbot, voice interaction, rule-based medical safety checks, and AIoT-ready ESP32/MAX30102 sensor monitoring support.