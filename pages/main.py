import streamlit as st

st.set_page_config(page_title="Main Page")

if "user" not in st.session_state or st.session_state.user is None:
    st.warning("You must log in first.")
    st.switch_page("auth.py")

st.title("🎉 Welcome!")
st.success(f"Hello {st.session_state.user.user.email} 👋")

if st.button("Logout"):
    st.session_state.user = None
    st.switch_page("auth.py")
