from agent_mail_fetcher import fetch_unread_emails
from agent_content_analyzer import analyze_email_content
from agent_storage import store_email_data
from google_calender import create_events_on_calendar

emails = fetch_unread_emails()

if not emails:
    print(" No unread emails found.")
else:
    for i, email in enumerate(emails):
        print(f"\n Email {i+1}")

        # Standardize the email structure
        standardized = {
            "subject": email.get("subject", ""),
            "sender": email.get("from", ""),
            "content": email.get("body", ""),
            "date_received": email.get("date", "")
        }

        # Analyze the content via LLM
        result = analyze_email_content(standardized)

        if result:
            # Print all extracted fields
            for k, v in result.items():
                print(f"🔹 {k}: {v}")
            print("=" * 50)

            # Store in SQLite DB
            store_email_data(standardized)
            print(" Stored in DB.")

            # Only if both date and time are present
            interview_dates = result.get("interview_dates", [])
            times = result.get("times", [])

            if interview_dates and times:
                create_events_on_calendar(
                    title=standardized.get("subject", "No Subject"),
                    description=result.get("summary", ""),
                    dates=interview_dates,
                    times=times
                )
                print(" Event added to calendar.")
            else:
                 print(" Failed to add to calendar.")
