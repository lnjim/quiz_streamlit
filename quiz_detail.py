import streamlit as st
import pandas as pd
from database import session, Quiz, QuizResult, Student

def show_quiz_detail(quiz_id):
    quiz = session.query(Quiz).filter_by(id=quiz_id).first()
    if not quiz:
        st.error("Quiz not found")
        return

    st.header(f"Quiz: {quiz.name}")

    if st.button("⬅️ Back to Class"):
        st.session_state["selected_quiz_id"] = None
        st.rerun()

    st.subheader("📥 Import Grades")
    st.write("CSV must have columns: `student_id`, `grade`")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if not all(col in df.columns for col in ["student_id", "grade"]):
            st.error("CSV must have columns: student_id, grade")
        else:
            imported = 0
            for _, row in df.iterrows():
                if pd.isna(row["student_id"]) or pd.isna(row["grade"]):
                    continue

                student = (
                    session.query(Student)
                    .filter_by(student_id=row["student_id"], class_id=quiz.class_id)
                    .first()
                )
                if not student:
                    continue

                result = (
                    session.query(QuizResult)
                    .filter_by(student_id=student.id, quiz_id=quiz.id)
                    .first()
                )
                if result:
                    result.grade = row["grade"]
                else:
                    new_result = QuizResult(student_id=student.id, quiz_id=quiz.id, grade=row["grade"])
                    session.add(new_result)
                imported += 1

            session.commit()
            st.success(f"{imported} grades imported successfully!")

    # --- Display results ---
    st.subheader("📊 Results")
    results = session.query(QuizResult).filter_by(quiz_id=quiz.id).all()
    if results:
        df_display = pd.DataFrame([
            {
                "Student": f"{r.student.first_name} {r.student.last_name}",
                "Grade": r.grade
            }
            for r in results
        ])
        st.dataframe(df_display, use_container_width=True)
        st.write(f"**Average Grade:** {df_display['Grade'].mean():.2f}")
    else:
        st.info("No grades yet.")
