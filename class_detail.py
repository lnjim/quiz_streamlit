import streamlit as st
import pandas as pd
from database import session, Class, Student, Quiz

def show_class_detail(class_id):
    # Fetch the class fresh from DB
    class_ = session.query(Class).filter_by(id=class_id).first()
    if not class_:
        st.error("Class not found")
        return

    # --- Header ---
    st.header(f"Class: {class_.name}")

    # --- Back button ---
    if st.button("⬅️ Back to Classes"):
        st.session_state["selected_class_id"] = None
        st.rerun()

    # --- Tabs for Students / Quizzes ---
    tab_students, tab_quizzes = st.tabs(["👨‍🎓 Students", "🧩 Quizzes"])

    # ===== STUDENTS TAB =====
    with tab_students:
        st.subheader("📥 Import students via CSV")
        st.write("CSV must have columns: `student_id`, `first_name`, `last_name`")

        uploaded_file = st.file_uploader("Choose a CSV file", type="csv", key=f"csv_{class_id}")
        added_count = 0

        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            required_cols = ["student_id", "first_name", "last_name"]
            if not all(col in df.columns for col in required_cols):
                st.error(f"CSV must have columns: {', '.join(required_cols)}")
            else:
                for _, row in df.iterrows():
                    # Skip rows with missing fields
                    if pd.isna(row["student_id"]) or pd.isna(row["first_name"]) or pd.isna(row["last_name"]):
                        continue

                    # Skip duplicate student_id
                    if session.query(Student).filter_by(student_id=row["student_id"]).first():
                        continue

                    student = Student(
                        student_id=row["student_id"],
                        first_name=row["first_name"],
                        last_name=row["last_name"],
                        class_id=class_id
                    )
                    session.add(student)
                    added_count += 1

                session.commit()
                st.success(f"{added_count} students imported successfully!")

        # --- Students list ---
        st.subheader("👨‍🎓 Student List")
        students = session.query(Student).filter_by(class_id=class_id).all()
        if students:
            student_data = [{"ID": s.student_id, "Name": f"{s.first_name} {s.last_name}"} for s in students]
            st.dataframe(student_data, use_container_width=True, hide_index=True)
        else:
            st.info("No students yet.")

    # ===== QUIZZES TAB =====
    with tab_quizzes:
        st.subheader("🧩 Create a new quiz")

        quiz_name = st.text_input("Quiz title", key=f"quiz_name_{class_id}")
        if st.button("Create quiz", key=f"create_quiz_{class_id}"):
            if quiz_name.strip() == "":
                st.error("Quiz title cannot be empty.")
            else:
                new_quiz = Quiz(name=quiz_name.strip(), class_id=class_id)
                session.add(new_quiz)
                session.commit()
                st.success(f"Quiz '{quiz_name}' created successfully!")
                st.rerun()

        # --- Quizzes list ---
        st.subheader("📚 Quiz List")
        quizzes = session.query(Quiz).filter_by(class_id=class_id).all()
        if quizzes:
            for q in quizzes:
                if st.button(f"View {q.name}", key=f"view_quiz_{q.id}"):
                    st.session_state.selected_quiz_id = q.id
                    st.session_state.view = "quiz_detail"
                    st.rerun()
        else:
            st.info("No quizzes yet.")
