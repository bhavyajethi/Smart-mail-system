import json
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

# === CONFIGURE GEMINI ===
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # Replace with secure key in production
model = genai.GenerativeModel("models/gemini-1.5-flash")

# === ANALYZE EMAIL CONTENT ===
def analyze_email_content(email):
    prompt = f"""
You are an AI assistant that summarizes emails and extracts structured fields.

EMAIL:
Subject: {email['subject']}
From: {email['sender']}
Content: {email['content']}

Return only a JSON object with these keys:
- summary (write a brief, natural-sounding summary in 2–3 lines like a human would write)
- companies (list of company names mentioned)
- interview_dates (list of date strings in YYYY-MM-DD)
- times (list of times in HH:MM 24hr format)
- is_actionable (true only if both date and time are present)

Only return the JSON object. No explanation, no formatting, no markdown.
"""

    try:
        response = model.generate_content(prompt)
        raw_text = response.text.strip()

        # Handle code fences if Gemini returns markdown block
        if raw_text.startswith("```json"):
            raw_text = raw_text.removeprefix("```json").removesuffix("```").strip()
        elif raw_text.startswith("```"):
            raw_text = raw_text.removeprefix("```").removesuffix("```").strip()

        # Parse JSON response
        data = json.loads(raw_text)

        # ✅ Recalculate is_actionable to ensure consistency
        if data.get("interview_dates") and data.get("times"):
            data["is_actionable"] = True
        else:
            data["is_actionable"] = False

        return data

    except Exception as e:
        print("❌ Error parsing Gemini response:", e)
        print("Raw output:\n", response.text if 'response' in locals() else 'No response')
        return None

import json
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

# === CONFIGURE GEMINI ===
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # Replace with secure key in production
model = genai.GenerativeModel("models/gemini-1.5-flash")

# === ANALYZE EMAIL CONTENT ===
def analyze_email_content(email):
    prompt = f"""
You are an AI assistant that summarizes emails and extracts structured fields.

EMAIL:
Subject: {email['subject']}
From: {email['sender']}
Content: {email['content']}

Return only a JSON object with these keys:
- summary (write a brief, natural-sounding summary in 2–3 lines like a human would write)
- companies (list of company names mentioned)
- interview_dates (list of date strings in YYYY-MM-DD)
- times (list of times in HH:MM 24hr format)
- is_actionable (true only if both date and time are present)

Only return the JSON object. No explanation, no formatting, no markdown.
"""

    try:
        response = model.generate_content(prompt)
        raw_text = response.text.strip()

        # Handle code fences if Gemini returns markdown block
        if raw_text.startswith("```json"):
            raw_text = raw_text.removeprefix("```json").removesuffix("```").strip()
        elif raw_text.startswith("```"):
            raw_text = raw_text.removeprefix("```").removesuffix("```").strip()

        # Parse JSON response
        data = json.loads(raw_text)

        # Recalculate is_actionable to ensure consistency
        if data.get("interview_dates") and data.get("times"):
            data["is_actionable"] = True
        else:
            data["is_actionable"] = False

        return data

    except Exception as e:
        print(" Error parsing Gemini response:", e)
        print("Raw output:\n", response.text if 'response' in locals() else 'No response')
        return None
