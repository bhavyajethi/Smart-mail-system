# from twilio.rest import Client
# from googleapiclient.discovery import build
# from agent_mail_fetcher import authenticate_gmail
# from google_calender import create_events_on_calendar
# from dotenv import load_dotenv
# import os
# import requests

# load_dotenv()

# DOCUMENT_ID = os.getenv("DOCUMENT_ID")
# ULTRA_MSG_INSTANCE_ID = os.getenv("ULTRA_MSG_INSTANCE_ID")
# ULTRA_MSG_TOKEN = os.getenv("ULTRA_MSG_TOKEN")


# def send_whatsapp_notification(subject, date, time):
#     if date != "No Date" and time != "No Time":
#         body = f"""📬 NEW EMAIL:
# Subject: {subject}
# Date(s): {date}
# Time(s): {time}
# 📅 Date and Time detected. Event added to calendar."""
#     elif date != "No Date" or time != "No Time":
#         body = f"""📬 NEW EMAIL:
# Subject: {subject}
# Date(s): {date}
# Time(s): {time}
# ⚠️ Only Date or Time detected. Not added to calendar."""
#     else:
#         body = f"""📬 NEW EMAIL:
# Subject: {subject}
# 📭 No Date or Time detected. Only added to Notes Doc."""

#     url = f"https://api.ultramsg.com/{ULTRA_MSG_INSTANCE_ID}/messages/chat"
#     payload = {
#         "token": ULTRA_MSG_TOKEN,
#         "to": os.getenv("WHATSAPP_NUMBER"),
#         "body": body
#     }

#     try:
#         response = requests.post(url, data=payload)
#         if response.status_code == 200:
#             print("✅ WhatsApp message sent.")
#         else:
#             print("❌ WhatsApp send failed:", response.json())
#     except Exception as e:
#         print("❌ UltraMsg error:", e)


# def store_email_data(email):
#     creds = authenticate_gmail()._http.credentials
#     docs_service = build('docs', 'v1', credentials=creds)

#     subject = email.get("subject", "")
#     sender = email.get("from", "")
#     body = email.get("body", "")
#     dates = email.get("dates", [])
#     times = email.get("times", [])

#     interview_dates = ', '.join(dates) if dates else "No Date"
#     time_str = ', '.join(times) if times else "No Time"
#     is_actionable = bool(dates and times)

#     send_whatsapp_notification(subject, interview_dates, time_str)

#     # ✅ Add to calendar if actionable
#     if is_actionable:
#         create_events_on_calendar(subject, body, dates, times)

#     msg_type = (
#         "📅 Date and time detected — Event added to calendar." if is_actionable
#         else "🕒 Partial info detected — Not added to calendar, but saved to notes."
#         if dates or times
#         else "❌ No date/time detected — Saved to notes."
#     )

#     doc_entry = f"""
# 📩 *New Email Summary*
# -----------------------------
# 🟢 Subject: {subject}
# ✉️ Sender: {sender}
# 📝 Summary: {body[:100]}...
# 📅 Dates: {interview_dates}
# ⏰ Times: {time_str}
# ✅ Actionable: {"Yes" if is_actionable else "No"}

# {msg_type}
# =============================

# """

#     try:
#         docs_service.documents().batchUpdate(
#             documentId=DOCUMENT_ID,
#             body={'requests': [{'insertText': {'location': {'index': 1}, 'text': doc_entry}}]}
#         ).execute()
#         print("📄 Stored in Google Docs.")
#     except Exception as e:
#         print("❌ Google Docs error:", e)



















from twilio.rest import Client
from googleapiclient.discovery import build
from agent_mail_fetcher import authenticate_gmail
from google_calender import create_events_on_calendar
from dotenv import load_dotenv
import os
import requests

load_dotenv()

DOCUMENT_ID = os.getenv("DOCUMENT_ID")
ULTRA_MSG_INSTANCE_ID = os.getenv("ULTRA_MSG_INSTANCE_ID")
ULTRA_MSG_TOKEN = os.getenv("ULTRA_MSG_TOKEN")


def send_whatsapp_notification(subject, dates, times):
    has_date = dates and dates != "No Date"
    has_time = times and times != "No Time"

    if has_date and has_time:
        body = f""" NEW EMAIL:
Subject: {subject}
Date(s): {dates}
Time(s): {times}
Date and Time detected. Event added to calendar."""
    elif has_date or has_time:
        body = f""" NEW EMAIL:
Subject: {subject}
Date(s): {dates}
Time(s): {times}
Only Date or Time detected. Not added to calendar."""
    else:
        body = f""" NEW EMAIL:
Subject: {subject}
Date(s): {dates}
Time(s): {times}
No Date or Time detected. Only added to Notes Doc."""

    url = f"https://api.ultramsg.com/{ULTRA_MSG_INSTANCE_ID}/messages/chat"
    payload = {
        "token": ULTRA_MSG_TOKEN,
        "to": os.getenv("WHATSAPP_NUMBER"),
        "body": body
    }

    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("WhatsApp message sent.")
        else:
            print("WhatsApp send failed:", response.json())
    except Exception as e:
        print("UltraMsg error:", e)


def store_email_data(email):
    creds = authenticate_gmail()._http.credentials
    docs_service = build('docs', 'v1', credentials=creds)

    subject = email.get("subject", "")
    sender = email.get("from", "")
    body = email.get("body", "")
    dates = email.get("interview_dates", [])  # ✅ Corrected key
    times = email.get("times", [])            # ✅ Already correct

    interview_dates = ', '.join(dates) if dates else "No Date"
    time_str = ', '.join(times) if times else "No Time"
    is_actionable = bool(dates and times)

    #  Send WhatsApp notification with correct values
    send_whatsapp_notification(subject, interview_dates, time_str)

    # Add to calendar if both date and time present
    if is_actionable:
        create_events_on_calendar(subject, body, dates, times)

    msg_type = (
        "Date and time detected — Event added to calendar." if is_actionable
        else " Partial info detected — Not added to calendar, but saved to notes."
        if dates or times
        else " No date/time detected — Saved to notes."
    )

    doc_entry = f"""
*New Email Summary*
-----------------------------
Subject: {subject}
Sender: {sender}
Summary: {body[:100]}...
Dates: {interview_dates}
Times: {time_str}
Actionable: {"Yes" if is_actionable else "No"}

{msg_type}
=============================

"""

    try:
        docs_service.documents().batchUpdate(
            documentId=DOCUMENT_ID,
            body={'requests': [{'insertText': {'location': {'index': 1}, 'text': doc_entry}}]}
        ).execute()
        print(" Stored in Google Docs.")
    except Exception as e:
        print(" Google Docs error:", e)
