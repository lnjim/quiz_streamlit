import streamlit as st
from database import session, Teacher
from utils import hash_password, check_password, validate_password
import re

def show_register():
    st.header("Register")
    username = st.text_input("Username")
    email = st.text_input("Email")

    # Password requirements info
    st.markdown(
        """
        **Password requirements:**
        - Minimum **8** characters
        - At least **1 uppercase** letter
        - At least **1 lowercase** letter
        - At least **1 number**
        - At least **1 special character** (`!@#$%^&*`)
        """,
        unsafe_allow_html=True
    )

    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if not username or not email or not password:
            st.error("Please fill in all fields")
            return
        if password != confirm_password:
            st.error("Passwords do not match")
            return
        if not validate_password(password):
            st.error("Password does not meet the required criteria.")
            return
        if session.query(Teacher).filter_by(email=email).first():
            st.error("Email already registered")
            return

        teacher = Teacher(
            username=username,
            email=email,
            password=hash_password(password)
        )
        session.add(teacher)
        session.commit()
        st.success("Account created successfully! Please switch to Login tab.")


def show_login():
    st.header("Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        teacher = session.query(Teacher).filter_by(email=email).first()
        if teacher and check_password(password, teacher.password):
            st.session_state.logged_in = True
            st.session_state.teacher_id = teacher.id
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error("Invalid email or password")
