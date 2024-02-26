from sqlalchemy import Integer, String, Date
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

# from connect_db import connect

# engine = connect()


class Base(DeclarativeBase):
    pass


student_groupe_assoc = Table(
    "student_groupe_assoc",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("student_id", Integer, ForeignKey("students.id", ondelete="CASCADE")),
    Column("groupe_id", Integer, ForeignKey("groupes.id", ondelete="CASCADE")),
)


class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)

    grades = relationship("Grade", back_populates="student")
    groupes = relationship(
        "Groupe", secondary=student_groupe_assoc, back_populates="students"
    )

    def __repr__(self) -> str:
        return f"id={self.id}, name={self.name}, groupe={self.groupes}"


class Groupe(Base):
    __tablename__ = "groupes"
    id: Mapped[int] = mapped_column(primary_key=True)
    groupe_name: Mapped[str] = mapped_column(String(5), nullable=False)

    students = relationship(
        "Student", secondary=student_groupe_assoc, back_populates="groupes"
    )

    def __repr__(self) -> str:
        return f"Groupe: id={self.id}, name={self.groupe_name}"


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)

    course = relationship("Course", back_populates="teacher")


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    course_name: Mapped[str] = mapped_column(String(100), nullable=False)
    teacher_id: Mapped[int] = mapped_column(
        ForeignKey("teachers.id", ondelete="CASCADE")
    )
    teacher = relationship("Teacher", back_populates="course")
    grades = relationship("Grade", back_populates="course")


class Grade(Base):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(primary_key=True)
    grade: Mapped[int] = mapped_column(nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)
    date_of: Mapped[Date] = mapped_column(Date, nullable=False)

    course = relationship("Course", back_populates="grades")
    student = relationship("Student", back_populates="grades")
