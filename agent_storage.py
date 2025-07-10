from twilio.rest import Client
from googleapiclient.discovery import build
from agent_mail_fetcher import authenticate_gmail  # Reuses same token flow
from dotenv import load_dotenv
import os

load_dotenv()

# Only needed for Docs API
SCOPES = ['https://www.googleapis.com/auth/documents']

DOCUMENT_ID = os.getenv("DOCUMENT_ID")  # Your Google Doc ID

# ✅ WhatsApp Notification
import requests

# ✅ UltraMsg Configuration
ULTRA_MSG_INSTANCE_ID = os.getenv("ULTRA_MSG_INSTANCE_ID")
ULTRA_MSG_TOKEN = os.getenv("ULTRA_MSG_TOKEN")

# ✅ WhatsApp Message Sender via UltraMsg
def send_whatsapp_notification(subject, date, time):
    # Determine message based on info presence
    if date != "No Date" and time != "No Time":
        body = f"""📬 NEW EMAIL:
Subject: {subject}
Date(s): {date}
Time(s): {time}
📅 Date and Time detected. Event added to calendar."""
    elif date != "No Date" or time != "No Time":
        body = f"""📬 NEW EMAIL:
Subject: {subject}
Date(s): {date}
Time(s): {time}
⚠️ Only Date or Time detected. Not added to calendar."""
    else:
        body = f"""📬 NEW EMAIL:
Subject: {subject}
📭 No Date or Time detected. Only added to Notes Doc."""

    # ✅ UltraMsg API request
    url = f"https://api.ultramsg.com/{ULTRA_MSG_INSTANCE_ID}/messages/chat"
    payload = {
        "token": ULTRA_MSG_TOKEN,
        "to": os.getenv("WHATSAPP_NUMBER"),  # Your WhatsApp number with country code
        "body": body
    }

    try:
        response = requests.post(url, data=payload)
        response_data = response.json()
        if response.status_code == 200 and response_data.get("sent"):
            print("✅ WhatsApp message sent via UltraMsg.")
        else:
            print("❌ Failed to send WhatsApp message:", response_data)
    except Exception as e:
        print("❌ UltraMsg API error:", e)


# ✅ Store to Google Docs instead of local DB
def store_email_data(email, extracted):
    creds = authenticate_gmail()._http.credentials  # Get credentials from Gmail service
    docs_service = build('docs', 'v1', credentials=creds)

    # Extract fields
    subject = email.get("subject", "")
    sender = email.get("sender", "")
    summary = extracted.get("summary", "")
    companies = ', '.join(extracted.get("companies", []))
    interview_dates = ', '.join(extracted.get("interview_dates", [])) or "No Date"
    times = ', '.join(extracted.get("times", [])) or "No Time"
    is_actionable = extracted.get("is_actionable", False)

    # ✅ Send WhatsApp Notification
    send_whatsapp_notification(subject, interview_dates, times)

    # Message type to insert in docs
    msg_type = (
        "📅 Date and time detected — Event added to calendar." if extracted["interview_dates"] and extracted["times"]
        else "🕒 Partial info detected — Not added to calendar, but saved to notes."
        if extracted["interview_dates"] or extracted["times"]
        else "❌ No date/time detected — Saved to notes."
    )

    # Format for Google Doc
    doc_entry = f"""
📩 *New Email Summary*
-----------------------------
🟢 Subject: {subject}
✉️ Sender: {sender}
📝 Summary: {summary}
🏢 Companies: {companies}
📅 Dates: {interview_dates}
⏰ Times: {times}
✅ Actionable: {"Yes" if is_actionable else "No"}

{msg_type}
=============================

"""

    # ✅ Append to Google Docs
    try:
        docs_service.documents().batchUpdate(
            documentId=DOCUMENT_ID,
            body={
                'requests': [
                    {
                        'insertText': {
                            'location': {'index': 1},
                            'text': doc_entry
                        }
                    }
                ]
            }
        ).execute()
        print("📄 Email data stored in Google Doc successfully.")
    except Exception as e:
        print("❌ Error storing email data in Google Doc:", e)
