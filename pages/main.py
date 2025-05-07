import streamlit as st
import os
from pathlib import Path
from pages.gmail_auth import authenticate_gmail
from pages.gmail_auth import Load_Cred

CRED_PATH= Path("secret/credential.json")
TOKEN_PATH= Path("secret/token.pickle")

st.set_page_config(page_title="Main Page")

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("You must log in first.")
    st.switch_page("login.py")
    
st.title("🎉 Welcome!")
st.success(f"Hello {st.session_state.user.user.email} 👋")

def save_uploaded_file(uploaded_file):
    save_dir = Path("./secret")  # Relative directory (safer than /secret)
    save_path = save_dir / "credential.json"

    # Ensure the directory exists
    save_dir.mkdir(parents=True, exist_ok=True)

    # Save the file
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"File saved to {save_path}")

#To Upload a OAuth Credential and store it in the session.
if CRED_PATH.exists():
    Load_Cred()
    st.switch_page("pages/app.py")

else:
    st.write("Upload your Gmail OAuth Token")
    uploaded_file = st.file_uploader("Choose a file", type="json")

    if uploaded_file:
        st.session_state['client_secrets_file']=uploaded_file
        st.success("File uploaded successfully!")
    else:
        st.warning("Upload the the Gmail Credentials")

    if st.button("Save Credentials File🗝️"):
        try:
            if uploaded_file:
                save_uploaded_file(uploaded_file)
            service = Load_Cred()
            st.success("✅ Gmail authentication successful!")
            st.switch_page("pages/app.py")

        except Exception as e:
            st.error(f"Saving Credential failed: {e}")

    if st.button("Continue Without Saving🔐"):
            try:
                service = authenticate_gmail()
                st.success("✅ Gmail authentication successful!")
                st.switch_page("pages/app.py")

            except Exception as e:
                st.error(f"Authentication failed: {e}")