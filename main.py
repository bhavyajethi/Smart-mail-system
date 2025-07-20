# main.py

import streamlit as st
from agent_mail_fetcher import fetch_unread_emails
from agent_content_analyzer import analyze_email_content
from agent_storage import store_email_data
from google_calender import create_events_on_calendar
from agent_storage import send_whatsapp_notification
import os

# --- Password Protection ---
st.set_page_config(page_title="Smart Mail Agent", layout="wide")
st.title("Smart Mail Agent for Bhavya Jethi")

password = st.text_input("Enter password to continue:", type="password")
if password != os.getenv("APP_PASSWORD"):
    st.warning("Incorrect or missing password.")
    st.stop()

# --- Main Logic ---
if st.button("Process My Emails"):
    emails = fetch_unread_emails()
    
    if not emails:
        st.success("No new emails found!")
    
    for i, email in enumerate(emails, start=1):
        st.subheader(f" Email {i}: {email.get('subject', 'No Subject')}")
        
        result = analyze_email_content(email)
        store_email_data(result)
        
        # Show extracted summary
        st.write("Summary:", result.get("summary"))
        st.write("Company:", result.get("companies"))
        st.write("Date:", result.get("interview_dates"))
        st.write("Time:", result.get("times"))
        
        if result.get("interview_dates") or result.get("times"):
            create_events_on_calendar(result)
        
        send_whatsapp_notification(result)

    st.success("Done processing all emails!")
