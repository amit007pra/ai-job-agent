import streamlit as st
from supabase import create_client
from supabase_env import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="Login/Signup", layout="centered", page_icon="🔏")

st.title("AI Job Application Agent🤖")

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user:
    st.switch_page("main.py")

tab1, tab2 = st.tabs(["Login🔐", "Sign Up🆕"])

with tab1:
    st.subheader("Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_pass")
    if st.button("Login"):
        try:
            user = supabase.auth.sign_in_with_password({"email": email, "password": password})
            st.session_state.user = user
            #st.session_state["credentials"]=None
            st.success("Login successful")
            st.switch_page("pages/main.py")

        except Exception as e:
            st.error(f"Login failed: {e}")

    with st.popover("Forgot Password?"):
        email = st.text_input("Enter your email address")
        if st.button("Send Reset Link"):
            try:
                # Attempt to send password reset email
                supabase.auth.reset_password_for_email(email,{"redirect_to": "http://localhost:8501/update-password",})
                email_sent=st.success("Reset link sent to your email ✉️")
            except Exception as e:
                    st.error(f"Failed to send reset link: {e}")
    
with tab2:
    st.subheader("Sign Up")
    email = st.text_input("Email", key="signup_email")
    password = st.text_input("Password", type="password", key="signup_pass")
    if st.button("Create Account"):
        try:
            supabase.auth.sign_up({"email": email, "password": password})
            st.success("Check your email to confirm.")
        except Exception as e:
            st.error(f"Signup failed: {e}")

def logout():
    response = supabase.auth.sign_out()
    st.session_state.user = None
    st.switch_page("login.py")