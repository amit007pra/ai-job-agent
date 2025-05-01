import streamlit as st
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import tempfile

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authenticate_gmail():
    creds = None

    # Check if already authenticated
    if "credentials" in st.session_state:
        creds = st.session_state["credentials"]

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Use uploaded file from session state
            if "client_secrets_file" not in st.session_state:
                st.error("Please upload your client_secret.json file first.")
                return None
            
            # Write uploaded file to a temp file so Google lib can use it
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(st.session_state["client_secrets_file"].getbuffer())
                tmp_path = tmp.name
            
            flow = InstalledAppFlow.from_client_secrets_file(tmp_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials
        st.session_state["credentials"] = creds
        st.session_state["token"] = creds.token

    # Return Gmail service
    return build('gmail', 'v1', credentials=creds)
