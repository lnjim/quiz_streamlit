import streamlit as st
from database import session, Teacher, Class

# Show teacher profile + classes + create class
def show_profile():
    teacher_id = st.session_state.get("teacher_id")
    if not teacher_id:
        st.error("No teacher logged in")
        return

    # If a class is selected, show class detail instead
    if st.session_state.get("selected_class_id"):
        from class_detail import show_class_detail
        show_class_detail(st.session_state["selected_class_id"])
        return

    teacher = session.query(Teacher).filter_by(id=teacher_id).first()
    if not teacher:
        st.error("Teacher not found")
        return

    # --- Header & info ---
    st.header(f"Welcome, {teacher.username}!")
    st.write(f"Email: {teacher.email}")

    # --- Logout button ---
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.teacher_id = None
        st.success("Logged out successfully!")
        st.rerun()

    st.divider()
    st.subheader("📚 Your Classes")

    # --- List existing classes ---
    teacher_classes = session.query(Class).filter_by(teacher_id=teacher_id).all()
    if teacher_classes:
        for c in teacher_classes:
            if st.button(f"{c.name} — {len(c.students)} student(s)", key=f"class_{c.id}"):
                st.session_state["selected_class_id"] = c.id
                st.rerun()
    else:
        st.info("You have no classes yet.")

    st.divider()

    # --- Button to open expander for creating new class ---
    if st.button("➕ Create New Class"):
        st.session_state["show_class_expander"] = True

    if st.session_state.get("show_class_expander"):
        with st.expander("Create a New Class", expanded=True):
            st.write("Fill out the class details below:")
            class_name = st.text_input("Class name")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Create"):
                    if not class_name.strip():
                        st.error("Please enter a class name.")
                    elif session.query(Class).filter_by(name=class_name.strip()).first():
                        st.error("Class name already exists.")
                    else:
                        new_class = Class(name=class_name.strip(), teacher_id=teacher_id)
                        session.add(new_class)
                        session.commit()
                        st.success("Class created successfully!")
                        st.session_state["show_class_expander"] = False
                        st.rerun()
            with col2:
                if st.button("Cancel"):
                    st.session_state["show_class_expander"] = False
                    st.rerun()
