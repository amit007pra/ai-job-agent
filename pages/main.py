import streamlit as st
import os
from pages.gmail_auth import authenticate_gmail

st.set_page_config(page_title="Main Page")

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("You must log in first.")
    st.switch_page("login.py")


st.title("🎉 Welcome!")
st.success(f"Hello {st.session_state.user.user.email} 👋")

#To Upload a OAuth Credential and store it in the session. 

st.write("Upload your Gmail OAuth Token")
uploaded_file = st.file_uploader("Choose a file", type="json")

if uploaded_file:
    st.session_state['client_secrets_file']=uploaded_file
    st.success("File uploaded successfully!")
else:
    st.warning("Upload the the Gmail Credentials")

st.write(st.session_state)

if st.button("Authenticate with Gmail📧"):
        try:
            service = authenticate_gmail()
            st.success("✅ Gmail authentication successful!")
            st.write(st.session_state)
        except Exception as e:
            st.error(f"Authentication failed: {e}")

if st.button("Logout"):
    st.session_state.user = None
    st.switch_page("login.py")