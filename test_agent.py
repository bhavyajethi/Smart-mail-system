from agent_mail_fetcher import fetch_unread_emails
from agent_content_analyzer import analyze_email_content
from agent_storage import store_email_data
from google_calender import create_events_on_calendar


emails = fetch_unread_emails()

if not emails:
    print("❌ No unread emails found.")
else:
    for i, email in enumerate(emails):
        print(f"\n📩 Email {i+1}")

        standardized = {
            "subject": email.get("subject", ""),
            "sender": email.get("from", ""),
            "content": email.get("body", ""),
            "date_received": email.get("date", "")
        }

        result = analyze_email_content(standardized)
        if result:
            for k, v in result.items():
                print(f"🔹 {k}: {v}")
            print("=" * 50)
            store_email_data(standardized, result)
            if result.get("interview_dates") and result.get("times"):
                create_events_on_calendar(
                    result.get("subject", ""),
                    result.get("summary", ""),
                    result.get("interview_dates", []),
                    result.get("times", [])
                )
            print("📥 Stored in DB.\n")
        else:
            print("⚠️ Could not process.")