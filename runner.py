from agent_mail_fetcher import fetch_unread_emails
from agent_content_analyzer import analyze_email_content
from agent_storage import store_email_data
from google_calender import create_events_on_calendar
from agent_storage import send_whatsapp_notification
import time

def run_loop():
    while True:
        print("Checking for new emails...")
        emails = fetch_unread_emails()
        for email in emails:
            result = analyze_email_content(email)
            store_email_data(result)
            
            if "interview_dates" in result or "times" in result:
                create_events_on_calendar(result)

            send_whatsapp_notification(result)
        time.sleep(900)  # Run every 15 minutes

if __name__ == "__main__":
    run_loop()
