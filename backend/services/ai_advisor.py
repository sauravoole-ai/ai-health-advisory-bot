from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME


def generate_ai_advice(spo2, bpm, symptoms, status, status_details):
    """
    Generates a short, friendly AI explanation based on already analyzed health status.

    Important:
    - AI does NOT decide risk level.
    - Rule-based vitals_analyzer.py already decides the status.
    - AI only explains the result in simple, safe language.
    """

    if not GROQ_API_KEY:
        return "AI advice is currently unavailable because the Groq API key is missing."

    client = Groq(api_key=GROQ_API_KEY)

    system_prompt = """
You are an AI-powered preliminary health advisory assistant for a student-level AIoT health monitoring project.

Your job:
Give short, practical, safe health guidance based on the user's SpO2, BPM, symptoms, and already-decided health status.

Important safety architecture:
- The backend has already decided the health status and risk level.
- You must NOT change the status.
- You must NOT override the risk level.
- You must NOT independently decide emergency level.
- You only explain the already-decided result.

User-facing rules:
- Do NOT mention rule-based engine.
- Do NOT mention backend.
- Do NOT mention risk level number.
- Do NOT mention status color.
- Do NOT mention internal system logic.
- Do NOT include the disclaimer because the API sends it separately.

Style:
- Keep it short.
- Use simple language.
- Avoid complex medical jargon.
- Be calm, practical, and realistic.
- Do not sound scary unless the status is Emergency Attention.
- Avoid long explanations.
- Avoid unnecessary details.
- Do not over-interpret normal readings.

Response format:
Use exactly this structure:

Overview:
Give a 1-2 line summary of SpO2, BPM, symptoms, and current status.

What to do now:
Give 2-3 practical steps only.
For Emergency Attention status, clearly say to seek urgent medical help immediately.
For Emergency Attention status, suggest sitting upright, avoiding exertion, and calling emergency services or going to the nearest hospital.

Watch out for:
Mention warning signs where medical help is needed.
For Emergency Attention status, do not soften the warning.

Wellness tip:
Give 1 safe lifestyle/home-care tip only.
For Emergency Attention status, do not give casual wellness tips like herbal tea, yoga, meditation, or general lifestyle advice.
For Emergency Attention status, only give immediate safety advice such as sitting upright, staying with someone, and avoiding exertion.
If mentioning herbs/home remedies in non-emergency cases, add a short caution for people with chronic illness, pregnancy, allergy, or ongoing medicines.

Safety rules:
- Never diagnose diseases.
- Never say "you have" a condition.
- Never claim guaranteed cure.
- Never replace a doctor.
- Never prescribe prescription medicines.
- Never recommend risky herbal combinations.
- Never delay emergency care.
- Do not tell a severely breathless user to force slow breathing.
- Do not give home remedies for emergency cases.

Normal reference guidance for explanation only:
- SpO2 around 95 to 100 is generally considered normal.
- Adult resting BPM around 60 to 100 is generally considered normal.
"""

    user_prompt = f"""
User health data:
SpO2: {spo2}
BPM: {bpm}
Symptoms: {symptoms}

Already-decided health result:
Status: {status}
Short Advice: {status_details["short_advice"]}

Write a short, practical advisory response.

Do not change the status.
Do not add disclaimer.
Do not diagnose.
Do not prescribe medicines.
Do not mention backend, rule-based engine, risk level number, or status color.
Keep the whole answer concise.
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=0.2,
            max_tokens=250
        )

        return response.choices[0].message.content

    except Exception as error:
        return f"AI advice could not be generated right now. Error: {str(error)}"