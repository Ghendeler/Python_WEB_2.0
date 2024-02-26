from pprint import pprint
from sqlalchemy import select
from sqlalchemy.sql import func, desc
from sqlalchemy.orm import sessionmaker

from connect_db import connect
from models import Course
from models import Grade
from models import Groupe
from models import Student
from models import Teacher
from models import student_groupe_assoc


def select_1():  # done
    """
    1. Найти 5 студентов с наибольшим средним баллом по всем предметам.
    """
    q = session.execute(
        select(Student.name, func.round(func.avg(Grade.grade), 2).label("avg"))
        .join(Student)
        .group_by(Student.name)
        .order_by(desc("avg"))
        .limit(5)
    ).mappings().all()

    pprint(q)


def select_2():  # done
    """
    2. Найти студента с наивысшим средним баллом по определенному предмету.
    """
    q = session.execute(
        select(Student.name, func.round(func.avg(Grade.grade), 2).label("avg"))
        .join(Student)
        .filter(Grade.course_id == 3)
        .group_by(Student.name)
        .order_by(desc("avg"))
    ).mappings().first()

    pprint(q)


def select_3():  # done
    """
    3. Найти средний балл в группах по определенному предмету.
    """
    q = session.execute(
        select(
            Groupe.groupe_name,
            func.round(func.avg(Grade.grade), 2).label("avg")
        )
        .join(Course)
        .join(Student)
        .join(student_groupe_assoc)
        .join(Groupe)
        .filter(Grade.course_id == 2)
        .group_by(Groupe.groupe_name)
        .order_by(desc("avg"), )
    ).mappings().all()

    pprint(q)


def select_4():  # done
    """
    4. Найти средний балл на потоке (по всей таблице оценок).
    """
    q = session.execute(
        select(
            Groupe.groupe_name,
            func.round(func.avg(Grade.grade), 2).label("avg")
        )
        .join(Student)
        .join(student_groupe_assoc)
        .join(Groupe)
        .group_by(Groupe.groupe_name)
    ).mappings().all()

    pprint(q)


def select_5():  # done
    """
    5. Найти какие курсы читает определенный преподаватель.
    """
    q = session.execute(
        select(Teacher.name, Course.course_name)
        .join(Course)
        .filter(Teacher.id == 3)
    ).mappings().all()

    pprint(q)


def select_6():  # done
    """
    6. Найти список студентов в определенной группе.
    """
    q = session.execute(
        select(Groupe.groupe_name, Student.name)
        .join(Student.groupes)
        .filter(Groupe.id == 1)
    ).mappings().all()

    n = 1
    for s in q:
        print(n, s)
        n += 1


def select_7():  # done
    """
    7. Найти оценки студентов в отдельной группе по определенному предмету.
    """
    q = (
        session.execute(
            select(
                Groupe.groupe_name,
                Course.course_name,
                Student.name,
                Grade.grade,
            )
            .join(Grade.course)
            .join(Student)
            .join(Student.groupes)
            .filter(Groupe.id == 1, Course.id == 2)
            .order_by(Grade.date_of)
        )
        .mappings()
        .all()
    )

    n = 1
    for s in q:
        print(n, s)
        n += 1


def select_8():  # Done
    """
    8. Найти средний балл, который ставит определенный преподаватель
        по своим предметам.
    """
    q = session.execute(
        select(
            Teacher.name,
            Course.course_name,
            func.round(func.avg(Grade.grade), 2).label("avg")
        )
        .join(Grade.course)
        .join(Course.teacher)
        .filter(Teacher.id == 3)
        .group_by(Teacher.name, Course.course_name)
    ).mappings().all()

    n = 1
    for s in q:
        print(n, s)
        n += 1


def select_9():  # Done
    """
    9. Найти список курсов, которые посещает определенный студент.
    """
    q = session.execute(
        select(
            Student.name,
            Course.course_name,
        )
        .join(Grade.student)
        .join(Grade.course)
        .filter(Student.id == 5)
        .group_by(Student.name, Course.course_name)
    ).mappings().all()

    n = 1
    for s in q:
        print(n, s)
        n += 1


def select_10():  # Done
    """
    10.Список курсов, которые определенному студенту читает
        определенный преподаватель.
    """
    q = session.execute(
        select(
            Student.name.label('student'),
            Teacher.name.label('teacher'),
            Course.course_name,
        )
        .join(Grade.course)
        .join(Grade.student)
        .join(Course.teacher)
        .filter(Student.id == 2, Teacher.id == 4)
    ).mappings().all()

    n = 1
    for s in q:
        print(n, s)
        n += 1


def select_11():  # Dane
    """
    11. Середній бал, який певний викладач ставить певному студентові.
    """
    q = session.execute(
        select(
            Teacher.name.label('teacher'),
            Student.name.label('student'),
            func.round(func.avg(Grade.grade), 2).label("avg")
        )
        .join(Grade.student)
        .join(Grade.course)
        .join(Course.teacher)
        .filter(Teacher.id == 2, Student.id == 14)
        .group_by('teacher', 'student')
    ).mappings().all()

    n = 1
    for s in q:
        print(n, s)
        n += 1


def select_12():
    """
    12. Оцінки студентів у певній групі з певного предмета
        на останньому занятті.
    """
    sub_q = session.execute(
        select(Grade.date_of)
        .join(Grade.course)
        .join(Grade.student)
        .join(Student.groupes)
        .filter(Groupe.id == 2, Course.id == 5)
        .order_by(desc(Grade.date_of))
    ).first()
    pprint(sub_q)

    q = session.execute(
        select(
            Groupe.groupe_name,
            Course.course_name,
            Student.name,
            Grade.grade,
            Grade.date_of
        )
        .join(Grade.course)
        .join(Grade.student)
        .join(Student.groupes)
        .filter(
            Groupe.id == 2,
            Course.id == 5,
            Grade.date_of == sub_q[0]
        )
    ).mappings().all()

    n = 1
    for s in q:
        print(n, s)
        n += 1


if __name__ == "__main__":
    engine = connect()
    Session = sessionmaker(bind=engine)
    session = Session()

    # select_1()
    # select_2()
    # select_3()
    # select_4()
    # select_5()
    # select_6()
    # select_7()
    # select_8()
    # select_9()
    # select_10()
    # select_11()
    select_12()
