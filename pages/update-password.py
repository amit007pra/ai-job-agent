import streamlit as st
from supabase import create_client
from supabase_env import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("Update Your Password")


# Capture the access token from the URL (automatically passed by Supabase)
params= st.query_params
st.write(params)
access_token=params["access_token"]
st.write(access_token)
if not access_token:
    st.error("Missing access token. Please use the link from your email.")
else:
    # Ask for the new password
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Update Password"):
        if not new_password or not confirm_password:
            st.warning("Please fill in both fields.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        else:
            try:
                # Temporarily create a session from the access token
                # Update the password
                response = supabase.auth.get_user(access_token)
                response=supabase.auth.update_user({"password": new_password})
                st.write(response)
                st.success("Your password has been updated successfully!")
                st.switch_page("login.py")
            except Exception as e:
                st.error(f"Failed to update password: {e}")