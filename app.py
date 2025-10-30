import streamlit as st
from database import init_db
from auth import show_register, show_login
from profile import show_profile

# Initialize DB
init_db()
st.title("Teacher Quiz Tracker App")

# Session state defaults
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "teacher_id" not in st.session_state:
    st.session_state.teacher_id = None

# Main logic
if st.session_state.logged_in:
    show_profile()
else:
    # Use Streamlit's tab component for Register/Login
    tab_register, tab_login = st.tabs(["📝 Register", "🔐 Login"])

    with tab_register:
        show_register()

    with tab_login:
        show_login()
