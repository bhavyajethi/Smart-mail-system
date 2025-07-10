import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="📬 Smart Mail Agent Dashboard", layout="wide")

st.title("📬 Smart Mail Agent Dashboard")
st.markdown("Easily view and demo your summarized emails and calendar entries.")

conn = sqlite3.connect("mail_records.db")


st.subheader("📋 Notes DB (All Emails)")
notes = pd.read_sql_query("SELECT * FROM processed_emails ORDER BY date_received DESC", conn)
st.dataframe(notes, use_container_width=True)

st.subheader("📅 Calendar DB (Actionable Events)")
calendar = pd.read_sql_query("SELECT * FROM processed_emails ORDER BY date_received DESC", conn)
st.dataframe(calendar, use_container_width=True)

conn.close()
