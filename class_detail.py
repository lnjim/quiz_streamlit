import streamlit as st
import pandas as pd
from database import session, Class, Student

def show_class_detail(class_id):
    # Fetch class fresh from DB
    class_ = session.query(Class).filter_by(id=class_id).first()
    if not class_:
        st.error("Class not found")
        return

    st.header(f"Class: {class_.name}")

    # --- Back button ---
    if st.button("⬅️ Back to Classes"):
        st.session_state["selected_class_id"] = None
        st.rerun()  # updated for Streamlit 1.51+

    # --- CSV Upload ---
    st.subheader("📥 Import students via CSV")
    st.write("CSV must have columns: `student_id`, `first_name`, `last_name`")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
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
    st.subheader("👨‍🎓 Students")
    students = session.query(Student).filter_by(class_id=class_id).all()
    if students:
        for s in students:
            st.write(f"{s.student_id} — {s.first_name} {s.last_name}")
    else:
        st.info("No students yet.")


