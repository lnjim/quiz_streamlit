import streamlit as st
from auth import show_login
from profile import show_profile
from class_detail import show_class_detail
from quiz_detail import show_quiz_detail

st.set_page_config(page_title="Quiz Manager", layout="wide")

# --- SESSION STATE INIT ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "selected_class_id" not in st.session_state:
    st.session_state.selected_class_id = None
if "selected_quiz_id" not in st.session_state:
    st.session_state.selected_quiz_id = None

# --- MAIN ROUTING LOGIC ---
if not st.session_state.logged_in:
    show_login()
else:
    # If quiz selected → show quiz detail
    if st.session_state.selected_quiz_id:
        show_quiz_detail(st.session_state.selected_quiz_id)
    # Else if class selected → show class detail
    elif st.session_state.selected_class_id:
        show_class_detail(st.session_state.selected_class_id)
    # Else → show profile
    else:
        show_profile()
