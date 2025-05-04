import streamlit as st
import pandas as pd
from pathlib import Path
from pages.gmail_auth import authenticate_gmail
from utils.email_sender import send_bulk_emails

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("You must log in first.")
    st.switch_page("login.py")

DATA_PATH = Path("data/recruiters.csv")

st.set_page_config(page_title="AI Job Application Agent", layout="centered")

st.title("🤖 Automated Job Application Agent")
st.write("Welcome! This application will contact multiple Hirings in a single click!")

def dataform():
    # Upload Dataset or Load existing
    if DATA_PATH.exists():
        df = pd.read_csv(DATA_PATH)
        st.success("Recruiter dataset loaded successfully!")
        st.dataframe(df)
    else:
        st.warning("No recruiter dataset found in `data/` folder.")

if st.button("Load recruiters data"):
    dataform()

if st.button("🚀 Send Emails to Recruiters"):
    service = authenticate_gmail()
    result = send_bulk_emails(service)
    st.success(result)

if st.button("Logout"):
    st.session_state.user = None
    st.switch_page("login.py")