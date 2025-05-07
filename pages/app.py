import streamlit as st
import pandas as pd
from pathlib import Path
from pages.gmail_auth import authenticate_gmail
from pages.gmail_auth import Load_Cred
from utils.email_sender import send_bulk_emails

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("You must log in first.")
    st.switch_page("login.py")

DATA_PATH = Path("data/recruiters.csv")
TOKEN=Path("secret/token.pickle")

st.set_page_config(page_title="AI Job Application Agent", layout="centered")

st.title("🤖 Automated Job Application Agent")
st.write("Welcome! This application will contact multiple Hirings in a single click!")

if st.button("Load recruiters data"):
    try:
        df = pd.read_csv(DATA_PATH)
        st.success("Recruiter dataset loaded successfully!")
        st.dataframe(df)
    except FileNotFoundError:
        st.warning("No recruiter dataset found in `data/` folder. Add a new recruiter")
    except Exception as e:
        st.error(f"An error occurred while loading the dataset: {str(e)}")
    
col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 Send Emails to Recruiters"):
        if TOKEN.exists():
            service=Load_Cred()
        else:
            service = authenticate_gmail()
        result = send_bulk_emails(service)
        st.success(result)

with col2:
    if st.button("Add Recruiter"):
        st.switch_page("pages/addnew.py")

if st.button("Update Resume"):
    new_resume=st.file_uploader("Upload your resume here:")
    if new_resume:
        save_dir = Path("./data") 
        save_path = save_dir / "Resume.pdf"

                # Ensure the directory exists
        save_dir.mkdir(parents=True, exist_ok=True)

                # Save the file
        with open(save_path, "wb") as f:
            f.write(new_resume.getbuffer())
        st.success(f"File uploaded Successfully")

if st.button("Logout"):
    st.session_state.user = None
    st.switch_page("login.py")