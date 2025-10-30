import streamlit as st
from database import session, Teacher

def show_profile():
    teacher_id = st.session_state.get("teacher_id")
    if not teacher_id:
        st.error("No teacher logged in")
        return

    teacher = session.query(Teacher).filter_by(id=teacher_id).first()
    if not teacher:
        st.error("Teacher not found")
        return

    st.header(f"Welcome, {teacher.username}!")
    st.write(f"Email: {teacher.email}")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.teacher_id = None
        st.success("Logged out successfully!")
        st.rerun()
