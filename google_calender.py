# google_calender.py

from datetime import datetime, timedelta
from googleapiclient.discovery import build
from agent_mail_fetcher import authenticate_gmail

# ✅ Create Events on Calendar
def create_events_on_calendar(subject, summary, dates, times):
    creds = authenticate_gmail()._http.credentials
    service = build('calendar', 'v3', credentials=creds)
    calendar_id = 'primary'  # Consistent calendar

    for date, time in zip(dates, times):
        try:
            start_dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            end_dt = start_dt + timedelta(hours=1)
            event = {
                'summary': subject,
                'description': summary,
                'start': {'dateTime': start_dt.isoformat(), 'timeZone': 'Asia/Kolkata'},
                'end': {'dateTime': end_dt.isoformat(), 'timeZone': 'Asia/Kolkata'},
            }
            service.events().insert(calendarId=calendar_id, body=event).execute()
            print(f"📅 Event created: {subject}, Date: {date}, Time: {time}")
        except Exception as e:
            print(f"Error creating event: {e}")