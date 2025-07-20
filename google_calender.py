from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import os
from requests.exceptions import HTTPError

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/calendar.events',
]


def get_calendar_credentials():
    creds = None
    if os.path.exists('token_calendar.json'):
        creds = Credentials.from_authorized_user_file('token_calendar.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token_calendar.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def create_events_on_calendar(title, description, dates, times):
    try:
        creds = get_calendar_credentials()
        service = build('calendar', 'v3', credentials=creds)
        calendar_id = 'primary'

        for date, time in zip(dates, times):
            start_dt = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            end_dt = start_dt + timedelta(hours=1)

            event = {
                'summary': title,
                'description': description,
                'start': {'dateTime': start_dt.isoformat(), 'timeZone': 'Asia/Kolkata'},
                'end': {'dateTime': end_dt.isoformat(), 'timeZone': 'Asia/Kolkata'}
            }

            service.events().insert(calendarId=calendar_id, body=event).execute()
            print(f" Calendar Event Created: {title} - {date} {time}")

    except HTTPError as error:
        print(f" Calendar creation error: {error}")
        return False
