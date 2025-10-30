import streamlit as st
from database import init_db
from auth import show_register, show_login

# Initialize DB
init_db()
st.title("Teacher Quiz Tracker App")

# --- Session state defaults ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "teacher_id" not in st.session_state:
    st.session_state.teacher_id = None
if "auth_tab" not in st.session_state:
    st.session_state.auth_tab = "Register"
if "selected_class_id" not in st.session_state:
    st.session_state.selected_class_id = None
if "show_class_expander" not in st.session_state:
    st.session_state.show_class_expander = False

# --- Main logic ---
if st.session_state.logged_in:
    # Show profile or class detail
    from profile import show_profile
    show_profile()

else:
    # --- Auth Tabs ---
    auth_tabs = st.tabs(["Register", "Login"])

    with auth_tabs[0]:
        st.session_state.auth_tab = "Register"
        show_register()

    with auth_tabs[1]:
        st.session_state.auth_tab = "Login"
        show_login()
