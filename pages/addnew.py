import streamlit as st
import pandas as pd
from pathlib import Path

# Setup
st.set_page_config(page_title="Add New Recruiter", layout="centered")
st.title("📝 Add New Recruiter Details")

DATA_PATH = Path("data/recruiters.csv")

# Form for input
with st.form("new_recruiter_form", clear_on_submit=True):
    company_name = st.text_input("Company Name")
    recruiter_name = st.text_input("Recruiter Name")
    recruiter_email = st.text_input("Recruiter Email")
    role = st.text_input("Role Hiring For")
    skills_required = st.text_input("Skills Required (comma-separated)")
    col1, col2 = st.columns(2)
    with col1:
        submit = st.form_submit_button("➕ Add Recruiter")
    with col2:
        if st.button("cancel"):
            st.switch_page("pages/app.py")

# Handle form submission
if submit:
    if not all([company_name, recruiter_name, recruiter_email, role, skills_required]):
        st.error("⚠️ Please fill in all the fields!")
    else:
        new_data = pd.DataFrame([{
            'company_name': company_name.strip(),
            'recruiter_name': recruiter_name.strip(),
            'recruiter_email': recruiter_email.strip(),
            'role': role.strip(),
            'skills_required': skills_required.strip(),
            'sent_flag': False
        }])

        # Ensure the directory exists
        DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

        # Load existing data if file exists, else create new
        if DATA_PATH.exists():
            try:
                df = pd.read_csv(DATA_PATH)
                df = pd.concat([df, new_data], ignore_index=True)
            except Exception as e:
                st.error(f"❌ Failed to read existing data: {e}")
                df = new_data
        else:
            df = new_data

        try:
            df.to_csv(DATA_PATH, index=False)
            st.success("✅ Recruiter details added successfully!")
            st.switch_page("pages/app.py")
        except Exception as e:
            st.error(f"❌ Failed to save data: {e}")
