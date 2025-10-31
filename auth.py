import streamlit as st
from database import session, Teacher
from utils import hash_password, check_password, validate_password

def show_login():
    st.title("🔐 Authentication")

    tab_login, tab_register = st.tabs(["Login", "Register"])

    # --- LOGIN TAB ---
    with tab_login:
        st.subheader("Login")

        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            teacher = session.query(Teacher).filter_by(email=email).first()
            if teacher and check_password(password, teacher.password):
                st.session_state.logged_in = True
                st.session_state.teacher_id = teacher.id
                st.success(f"Welcome {teacher.username}!")
                st.rerun()
            else:
                st.error("Invalid email or password")

    # --- REGISTER TAB ---
    with tab_register:
        st.subheader("Register")

        username = st.text_input("Username", key="register_username")
        email = st.text_input("Email", key="register_email")

        st.markdown("""
        **Password requirements:**
        - At least 8 characters
        - One uppercase letter
        - One lowercase letter
        - One digit
        - One special character (!@#$%^&*)
        """)

        password = st.text_input("Password", type="password", key="register_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="register_confirm_password")

        if st.button("Register"):
            if not all([username, email, password, confirm_password]):
                st.error("All fields are required")
            elif password != confirm_password:
                st.error("Passwords do not match")
            elif not validate_password(password):
                st.error("Password does not meet requirements")
            elif session.query(Teacher).filter_by(email=email).first():
                st.error("Email already registered")
            else:
                hashed_pw = hash_password(password)
                new_teacher = Teacher(username=username, email=email, password=hashed_pw)
                session.add(new_teacher)
                session.commit()

                # Show flash success message under the Register form
                st.success("✅ Account created successfully! Please click on the Login tab to sign in.")
