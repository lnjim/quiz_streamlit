from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
engine = create_engine('sqlite:///quiz_app.db', echo=False)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# Teacher table
class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String)

# Class table
class Class(Base):
    __tablename__ = "classes"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    students = relationship("Student", back_populates="class_")

# Student table
class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    student_id = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    class_id = Column(Integer, ForeignKey("classes.id"))
    class_ = relationship("Class", back_populates="students")
    quizzes = relationship("QuizResult", back_populates="student")

# Quiz table
class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    class_id = Column(Integer, ForeignKey("classes.id"))
    results = relationship("QuizResult", back_populates="quiz")

# Quiz result table
class QuizResult(Base):
    __tablename__ = "quiz_results"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    grade = Column(Float)
    student = relationship("Student", back_populates="quizzes")
    quiz = relationship("Quiz", back_populates="results")

def init_db():
    Base.metadata.create_all(bind=engine)
