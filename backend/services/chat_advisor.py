from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME


DISCLAIMER = "This is not a medical diagnosis. Please consult a qualified healthcare professional for proper evaluation."


def check_emergency_message(user_message):
    message = user_message.lower()

    emergency_keywords = [
        "chest pain",
        "severe breathlessness",
        "breathlessness",
        "difficulty breathing",
        "shortness of breath",
        "fainting",
        "unconscious",
        "unconsciousness",
        "bluish lips",
        "blue lips",
        "confusion",
        "severe bleeding",
        "stroke",
        "very low spo2",
        "spo2 below 90",
        "spo2 less than 90",
        "oxygen below 90",
        "oxygen level below 90",
        "seizure",
        "severe allergic reaction"
    ]

    for keyword in emergency_keywords:
        if keyword in message:
            return True

    return False


def get_emergency_response():
    return {
        "status": "success",
        "reply": """Possible concern:
Your symptoms may need urgent medical attention. Chest pain, severe breathlessness, fainting, bluish lips, confusion, or very low SpO2 should not be handled with home remedies.

What you can do now:
1. Call emergency services or go to the nearest hospital immediately.
2. Sit upright and avoid physical exertion.
3. Stay with someone nearby if possible.
4. Do not delay medical care.

Please answer these:
If someone is with you, tell them your symptoms clearly and ask them to help you reach medical care.

When to seek medical help:
Seek urgent medical help immediately. Do not wait for the symptoms to worsen.""",
        "disclaimer": DISCLAIMER
    }


def check_identity_question(user_message):
    message = user_message.lower().strip()

    identity_keywords = [
        "who are you",
        "what are you",
        "your name",
        "what is your name",
        "who made you",
        "who created you",
        "what can you do",
        "how can you help",
        "who taught you",
        "who trained you",
        "are you doctor",
        "are you a doctor",
        "are you medical",
        "are you real doctor"
    ]

    for keyword in identity_keywords:
        if keyword in message:
            return True

    return False


def get_identity_response():
    return {
        "status": "success",
        "reply": """Possible concern:
This is not a symptom-related question.

What you can do now:
I am an AI-powered preliminary health advisory assistant. I can help explain basic health queries, symptoms, SpO2, BPM, and general wellness guidance in simple language.

Please answer these:
You can tell me your symptoms, duration, age, SpO2, BPM, fever status, or any health concern you want preliminary guidance about.

When to seek medical help:
If you have serious symptoms such as chest pain, severe breathlessness, fainting, bluish lips, confusion, very low SpO2, or severe weakness, seek urgent medical help immediately.""",
        "disclaimer": DISCLAIMER
    }


def check_health_related_message(user_message):
    message = user_message.lower()

    health_keywords = [
        "health",
        "sick",
        "ill",
        "illness",
        "symptom",
        "symptoms",
        "fever",
        "cold",
        "cough",
        "throat",
        "pain",
        "ache",
        "headache",
        "body pain",
        "weak",
        "weakness",
        "tired",
        "fatigue",
        "dizzy",
        "dizziness",
        "vomit",
        "vomiting",
        "nausea",
        "loose motion",
        "diarrhea",
        "constipation",
        "breathing",
        "breath",
        "spo2",
        "oxygen",
        "bpm",
        "pulse",
        "heart rate",
        "heartbeat",
        "blood pressure",
        "bp",
        "temperature",
        "sweating",
        "chills",
        "sleep",
        "dehydration",
        "hydration",
        "diet",
        "food",
        "water",
        "rest",
        "medicine",
        "medication",
        "doctor",
        "hospital",
        "emergency",
        "ayurveda",
        "home remedy",
        "remedy",
        "wellness",
        "fitness",
        "exercise",
        "stress",
        "anxiety",
        "allergy",
        "infection",
        "rash",
        "stomach",
        "chest",
        "lungs",
        "normal spo2",
        "normal bpm"
    ]

    for keyword in health_keywords:
        if keyword in message:
            return True

    return False


def check_followup_message(user_message, history):
    """
    Allows short follow-up answers like:
    - 5 days
    - since yesterday
    - 22 years
    - yes
    - no
    - mild fever
    - 97 spo2
    when previous chat history exists.
    """

    if not history or not isinstance(history, list):
        return False

    message = user_message.lower().strip()

    followup_keywords = [
        "yes",
        "no",
        "yesterday",
        "today",
        "morning",
        "night",
        "evening",
        "days",
        "day",
        "hours",
        "hour",
        "weeks",
        "week",
        "months",
        "month",
        "mild",
        "moderate",
        "severe",
        "high",
        "low",
        "normal",
        "since",
        "age",
        "years",
        "year",
        "spo2",
        "bpm",
        "fever",
        "cough",
        "pain",
        "weakness",
        "dizziness",
        "headache"
    ]

    if any(char.isdigit() for char in message):
        return True

    for keyword in followup_keywords:
        if keyword in message:
            return True

    if len(message.split()) <= 5:
        return True

    return False


def check_only_number(user_message):
    """
    Checks if user sent only a plain number like:
    30
    98
    5

    Such replies are ambiguous in a health chatbot.
    """

    message = user_message.strip()

    if message.replace(".", "", 1).isdigit():
        return True

    return False


def get_number_clarification_response(user_message):
    """
    Fixed response when the user sends only a number.
    """

    return {
        "status": "success",
        "reply": f"""Possible concern:
You entered only "{user_message}", but I cannot safely understand what this number means.

What you can do now:
Please send the number with a clear label so I do not assume incorrectly.

Please answer these:
- Is this your age? Example: Age: {user_message}
- Is this your temperature? Example: Temperature: {user_message}°F or {user_message}°C
- Is this your SpO2? Example: SpO2: {user_message}
- Is this your BPM? Example: BPM: {user_message}
- Is this the duration? Example: Duration: {user_message} days

When to seek medical help:
Seek medical help if you have high fever, breathing difficulty, chest pain, fainting, low SpO2, severe weakness, or worsening symptoms.""",
        "disclaimer": DISCLAIMER
    }


def get_out_of_scope_response():
    return {
        "status": "success",
        "reply": """Possible concern:
This question is outside my health advisory scope.

What you can do now:
I am designed to help with preliminary health guidance, symptoms, SpO2, BPM, and general wellness-related questions.

Please answer these:
If you want health guidance, tell me your symptoms, duration, age, SpO2, BPM, fever status, or other health concern.

When to seek medical help:
If you have serious symptoms such as chest pain, severe breathlessness, fainting, bluish lips, confusion, very low SpO2, or severe weakness, seek urgent medical help immediately.""",
        "disclaimer": DISCLAIMER
    }


def clean_chat_history(history):
    if not isinstance(history, list):
        return []

    cleaned_history = []

    for item in history:
        if not isinstance(item, dict):
            continue

        role = item.get("role")
        content = item.get("content")

        if role not in ["user", "assistant"]:
            continue

        if not content or not isinstance(content, str):
            continue

        cleaned_history.append({
            "role": role,
            "content": content
        })

    return cleaned_history[-6:]


def contains_medicine_advice(ai_reply):
    reply_lower = ai_reply.lower()

    medicine_keywords = [
        "acetaminophen",
        "ibuprofen",
        "paracetamol",
        "dolo",
        "aspirin",
        "antibiotic",
        "antibiotics",
        "pain reliever",
        "pain relievers",
        "painkiller",
        "painkillers",
        "tablet",
        "tablets",
        "capsule",
        "capsules",
        "dose",
        "dosage",
        "take medicine",
        "take medication",
        "over-the-counter",
        "otc",
        "nitroglycerin"
    ]

    for keyword in medicine_keywords:
        if keyword in reply_lower:
            return True

    return False


def get_safe_medicine_filtered_reply():
    return """Possible concern:
Your symptoms may be due to a common short-term issue such as tiredness, dehydration, poor sleep, mild infection, or general weakness. I cannot confirm the exact cause without proper medical evaluation.

What you can do now:
1. Rest and avoid heavy physical activity for now.
2. Drink enough water and take light, balanced food.
3. Monitor your temperature, SpO2, BPM, and symptom changes if possible.
4. Avoid self-medicating. For medicines, consult a qualified healthcare professional or pharmacist.

Please answer these:
- What is your age?
- Since when are you feeling this?
- Do you have fever, cough, throat pain, body ache, dizziness, chest pain, or breathing difficulty?
- What are your current SpO2 and BPM readings, if available?

When to seek medical help:
Seek medical help if symptoms worsen, fever remains high, breathing difficulty occurs, SpO2 becomes low, chest pain appears, fainting occurs, or weakness becomes severe."""


def ensure_response_format(ai_reply):
    required_heading = "When to seek medical help:"

    if required_heading.lower() not in ai_reply.lower():
        ai_reply = ai_reply.strip() + """

When to seek medical help:
Seek medical help if symptoms worsen, fever remains high, breathing difficulty occurs, chest pain appears, SpO2 becomes low, fainting occurs, or weakness becomes severe."""

    return ai_reply


def generate_chat_response(user_message, history=None):
    if not GROQ_API_KEY:
        return {
            "status": "error",
            "reply": "AI chat is currently unavailable because the Groq API key is missing.",
            "disclaimer": DISCLAIMER
        }

    if not user_message or not isinstance(user_message, str):
        return {
            "status": "error",
            "reply": "Please enter a valid health question or symptom description.",
            "disclaimer": DISCLAIMER
        }

    if check_emergency_message(user_message):
        return get_emergency_response()

    if check_identity_question(user_message):
        return get_identity_response()

    if check_only_number(user_message):
        return get_number_clarification_response(user_message)

    if not check_health_related_message(user_message):
        if not check_followup_message(user_message, history):
            return get_out_of_scope_response()

    client = Groq(api_key=GROQ_API_KEY)

    system_prompt = """
You are an AI-powered preliminary health advisory assistant.

Your role:
Help users with simple, safe, realistic, preliminary health guidance.

Core safety identity:
- You are not a doctor.
- You do not diagnose.
- You do not prescribe.
- You do not replace a qualified healthcare professional.
- You provide general preliminary guidance only.
- Stay within health, symptoms, vitals, wellness, SpO2, BPM, and safety guidance.

Anti-hallucination rules:
- Do not invent details that the user did not provide.
- Do not assume the user's age, gender, medical history, diagnosis, medicine use, temperature, SpO2, BPM, or severity.
- If the user sends only a number, do not assume what it means. Ask whether it refers to age, temperature, SpO2, BPM, or duration.
- Do not answer unrelated general knowledge, math, coding, entertainment, politics, or personal questions.
- If the question is outside health guidance, politely redirect to health-related use.
- Do not say "you have" a disease or condition.
- Do not strongly claim the cause of symptoms.
- Use cautious wording such as "may be related to", "can happen due to", or "I cannot confirm the exact cause".
- If important details are missing, ask follow-up questions instead of guessing.
- If the user provides very limited information, keep the answer general and ask for more details.
- Do not provide rare disease explanations unless the user's symptoms clearly suggest urgent medical review.
- Do not give long lists of possible diseases.
- Do not create fake certainty.

Medicine safety rules:
- Do not prescribe prescription medicines.
- Do not mention prescription medicine names.
- Do not mention over-the-counter medicine names.
- Do not suggest taking any medicine.
- Do not suggest painkillers, tablets, capsules, dose, or dosage.
- For medicine-related guidance, only say: "Please consult a qualified healthcare professional or pharmacist."

Emergency behavior:
If the user mentions chest pain, severe breathlessness, unconsciousness, fainting, bluish lips, confusion, severe bleeding, stroke-like symptoms, very low SpO2, or any life-threatening symptom:
- Clearly advise immediate medical help.
- Tell them to call emergency services or go to the nearest hospital.
- Do not give casual home remedies.
- Do not suggest medicines.
- Do not soften the warning.

Conversation behavior:
- Continue the conversation using the previous chat history if provided.
- Treat labeled replies like "Age: 30", "Duration: 5 days", "Temperature: 101°F", "SpO2: 97", or "BPM: 88" as follow-up answers when history exists.
- If the user answers your earlier question, use that answer naturally.
- Do not repeat the same follow-up questions unnecessarily.
- Ask about age, duration, severity, fever, SpO2, BPM, breathing difficulty, chest pain, fainting, existing illness, or ongoing medicines when relevant.
- Keep the reply simple and understandable for a normal person.
- Be practical, calm, and realistic.

For mild/common symptoms:
- Suggest rest, hydration, monitoring, light food, and safe general care.
- Mention when to consult a healthcare professional.
- Home remedies may be mentioned only if safe and simple.
- If mentioning herbs/home remedies, add caution for pregnancy, allergy, chronic illness, or ongoing medicines.

Response format:
Use exactly this structure:

Possible concern:
Briefly explain what the symptoms may generally indicate without diagnosing. Include uncertainty if details are limited.

What you can do now:
Give 2-4 practical steps.

Please answer these:
Ask 2-4 useful follow-up questions if more details are needed.

When to seek medical help:
Mention warning signs clearly.

Do not skip the medical-help section.
Do not include the medical disclaimer because it is sent separately by the API.
Keep the whole answer concise.
"""

    cleaned_history = clean_chat_history(history)

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    messages.extend(cleaned_history)

    messages.append({
        "role": "user",
        "content": user_message
    })

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.1,
            max_tokens=330
        )

        ai_reply = response.choices[0].message.content

        if contains_medicine_advice(ai_reply):
            ai_reply = get_safe_medicine_filtered_reply()

        ai_reply = ensure_response_format(ai_reply)

        return {
            "status": "success",
            "reply": ai_reply,
            "disclaimer": DISCLAIMER
        }

    except Exception as error:
        return {
            "status": "error",
            "reply": f"AI chat response could not be generated right now. Error: {str(error)}",
            "disclaimer": DISCLAIMER
        }