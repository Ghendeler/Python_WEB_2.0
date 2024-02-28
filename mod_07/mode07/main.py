import argparse

from pprint import pprint
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from connect_db import connect
from models import Course, Grade, Groupe, Student, Teacher


def create_data(**kwargs):
    engine = connect()
    Session = sessionmaker(bind=engine)
    session = Session()

    if kwargs["model"] == "teacher":
        teacher = Teacher(name=kwargs["name"])
        session.add(teacher)
    elif kwargs["model"] == "student":
        student = Student(name=kwargs["name"])
        session.add(student)
    elif kwargs["model"] == "groupe":
        groupe = Groupe(groupe_name=kwargs["name"])
        session.add(groupe)
    elif kwargs["model"] == "course":
        course = Course(course_name=kwargs["name"])
        session.add(course)

    session.commit()


def read_data(**kwargs):
    engine = connect()
    Session = sessionmaker(bind=engine)
    session = Session()

    if kwargs["model"] == "teacher":
        teachers = session.execute(select(Teacher.id, Teacher.name)).mappings().all()
        pprint(teachers)
    elif kwargs["model"] == "student":
        students = session.execute(select(Student.id, Student.name)).mappings().all()
        print(students)
    elif kwargs["model"] == "groupe":
        groupes = (
            session.execute(select(Groupe.id, Groupe.groupe_name)).mappings().all()
        )
        print(groupes)
    elif kwargs["model"] == "course":
        courses = (
            session.execute(select(Course.id, Course.course_name)).mappings().all()
        )
        print(courses)


def update_data(**kwargs):
    id = kwargs["id"]
    name = kwargs["name"]
    engine = connect()
    Session = sessionmaker(bind=engine)
    session = Session()

    if kwargs["model"] == "teacher":
        teacher = session.get(Teacher, id)
        teacher.name = name
    elif kwargs["model"] == "student":
        student = session.get(Student, id)
        student.name = name
    elif kwargs["model"] == "groupe":
        groupe = session.get(Groupe, id)
        groupe.name = name
    elif kwargs["model"] == "course":
        course = session.get(Course, id)
        course.name = name

    session.commit()


def delete_data(**kwargs):
    id = kwargs["id"]
    engine = connect()
    Session = sessionmaker(bind=engine)
    session = Session()

    if kwargs["model"] == "teacher":
        teacher = session.get(Teacher, id)
        session.delete(teacher)
    elif kwargs["model"] == "student":
        student = session.get(Student, id)
        session.delete(student)
    elif kwargs["model"] == "groupe":
        groupe = session.get(Groupe, id)
        session.delete(groupe)
    elif kwargs["model"] == "course":
        course = session.get(Course, id)
        session.delete(course)
    session.commit()


ACTION = {
    "create": create_data,
    "list": read_data,
    "update": update_data,
    "remove": delete_data,
}

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--action", required=True, choices=[k for k in ACTION.keys()])
parser.add_argument("-m", "--model")
parser.add_argument("--id", type=int)
parser.add_argument("--name")


def get_action_handler(action):
    return ACTION.get(action)


def insert_data_to_db(students, teachers, courses, groupes, grades):

    students_obgs = [Student(name=s[0]) for s in students]
    teachers_obgs = [Teacher(name=s[0]) for s in teachers]
    courses_obgs = [Course(course_name=s[0], teacher_id=s[1]) for s in courses]
    groupes_obgs = [Groupe(groupe_name=s[0]) for s in groupes]
    grades_obgs = [
        Grade(grade=s[0], student_id=s[1], course_id=s[2], date_of=s[3]) for s in grades
    ]

    for n in range(len(students_obgs)):
        students_obgs[n].groupes.append(groupes_obgs[randint(0, NUMBER_GROUPES - 1)])

    engine = connect()
    Session = sessionmaker(bind=engine)
    session = Session()

    session.add_all(students_obgs)
    session.add_all(teachers_obgs)
    session.add_all(courses_obgs)
    session.add_all(groupes_obgs)
    session.add_all(grades_obgs)
    session.commit()


def main():
    args = parser.parse_args()
    print(args)
    print(args.action)
    action_handler = get_action_handler(args.action)
    action_handler(**vars(args))


if __name__ == "__main__":
    main()
