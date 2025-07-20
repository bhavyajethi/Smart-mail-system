import os.path
import base64
from email import message_from_bytes
from email.header import decode_header
from bs4 import BeautifulSoup
import dateparser

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Gmail API Scope: read-only
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/documents']

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def decode_subject(subject):
    decoded = decode_header(subject)
    subject_str = ''
    for part, encoding in decoded:
        if isinstance(part, bytes):
            part = part.decode(encoding or 'utf-8', errors='ignore')
        subject_str += part
    return subject_str

def extract_body(mime_msg):
    body = ''
    if mime_msg.is_multipart():
        for part in mime_msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if content_type == 'text/plain' and 'attachment' not in content_disposition:
                body += part.get_payload(decode=True).decode('utf-8', errors='ignore')
                break
            elif content_type == 'text/html' and not body:
                html_body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                soup = BeautifulSoup(html_body, 'html.parser')
                body = soup.get_text()
    else:
        body = mime_msg.get_payload(decode=True).decode('utf-8', errors='ignore')
    return body.strip()

def extract_dates(body):
    dates = []
    for line in body.splitlines():
        date_match = dateparser.parse(line)
        if date_match:
            dates.append(date_match.strftime("%Y-%m-%d"))
    return dates

import re

def extract_times(body):
    times = []
    time_patterns = [
        r'\b\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)?',
        r'\b\d{1,2}(?:AM|PM|am|pm)\b',
    ]
    for line in body.splitlines():
        for pattern in time_patterns:
            matches = re.findall(pattern, line)
            times.extend(matches)
    return times

def fetch_unread_emails():
    service = authenticate_gmail()
    results = service.users().messages().list(
        userId='me',
        labelIds=['INBOX'],
        q='is:unread category:primary',
        maxResults=1
    ).execute()

    messages = results.get('messages', [])
    email_data = []

    for msg in messages:
        msg_id = msg['id']
        raw_msg_data = service.users().messages().get(userId='me', id=msg_id, format='raw').execute()
        raw_msg = base64.urlsafe_b64decode(raw_msg_data['raw'].encode("ASCII"))
        mime_msg = message_from_bytes(raw_msg)

        subject = decode_subject(mime_msg['subject'])
        sender = mime_msg['from']
        date = mime_msg['date']
        body = extract_body(mime_msg)
        dates = extract_dates(body)
        times = extract_times(body)

        email_data.append({
            "subject": subject,
            "from": sender,
            "date": date,
            "body": body,
            "dates": dates,
            "times": times
        })

    return email_data
