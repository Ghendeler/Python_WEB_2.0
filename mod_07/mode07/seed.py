from datetime import datetime
from random import choice, randint

from faker import Faker
from sqlalchemy.orm import sessionmaker

from connect_db import connect
from models import Course, Grade, Groupe, Student, Teacher


NUMBER_STUDENTS = 50
NUMBER_GROUPES = 3
NUMBER_COURSES = 8
NUMBER_TEACHERS = 5
NUMBER_GRADES = 20


def generate_fake_data(number_students, number_teachers,
                       number_courses, number_groupes) -> tuple():
    fake_students = []  # здесь будем хранить студентов
    fake_teachers = []  # здесь будем хранить преподавателей
    fake_courses = []  # здесь будем хранить курсы
    fake_groupes = []  # здесь будем хранить группы

    fake_data = Faker('uk_UA')

    # Создаем список студентов в количестве number_students
    for _ in range(number_students):
        fake_students.append(fake_data.name())

    # Создаем список преподавателей в количестве number_teachers
    for _ in range(number_teachers):
        fake_teachers.append(fake_data.name())

    # Создаем список курсов в количестве number_courses
    for _ in range(number_courses):
        fake_courses.append(fake_data.job())

    # Создаем список групп в количестве fake_groupes
    for _ in range(number_groupes):
        fake_groupes.append(fake_data.bothify(text='??-##', letters='ABCDE'))

    return fake_students, fake_teachers, fake_courses, fake_groupes


def prepare_data(students, teachers, courses, groupes) -> tuple():

    # подготавливаем список кортежей студентов
    for_students = []
    for student in students:
        for_students.append((student, ))

    # подготавливаем список кортежей преподавателей
    for_teachers = []
    for teacher in teachers:
        for_teachers.append((teacher, ))

    # подготавливаем список кортежей названий предметов
    # с преподавателем, который читает предмет
    for_courses = []
    for course in courses:
        for_courses.append((course, randint(1, NUMBER_TEACHERS)))

    # подготавливаем список кортежей групп
    for_groupes = []
    for groupe in groupes:
        for_groupes.append((groupe, ))

    # подготавливаем список кортежей оценок, где у каждого студента
    # есть оценки по предметам с указанием когда оценка получена,
    # до 20 оценок у каждого студента по всем предметам
    for_grades = []
    for student_id in range(1, NUMBER_STUDENTS + 1):
        for _ in range(NUMBER_GRADES):
            date = datetime(2023, choice([3, 4, 5]), randint(1, 30)).date()
            for_grades.append((randint(5, 12), student_id,
                               randint(1, NUMBER_COURSES), date))
    for_grades.sort(key=lambda d: d[3])

    return for_students, for_teachers, for_courses, for_groupes, for_grades


def insert_data_to_db(students, teachers, courses, groupes, grades) -> None:

    students_obgs = [Student(name=s[0]) for s in students]
    teachers_obgs = [Teacher(name=s[0]) for s in teachers]
    courses_obgs = [Course(course_name=s[0], teacher_id=s[1]) for s in courses]
    groupes_obgs = [Groupe(groupe_name=s[0]) for s in groupes]
    grades_obgs = [Grade(grade=s[0], student_id=s[1], course_id=s[2], date_of=s[3]) for s in grades]

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

    # print(students)
    # print(teachers)
    # print(courses)
    # print(groupes)

    students, teachers, courses, groupes, grades = prepare_data(
        *generate_fake_data(NUMBER_STUDENTS, NUMBER_TEACHERS,
                            NUMBER_COURSES, NUMBER_GROUPES))
    # print(students, '\n')
    # print(teachers, '\n')
    # print(courses, '\n')
    # print(groupes, '\n')
    # print(grades, '\n')

    insert_data_to_db(students, teachers, courses, groupes, grades)


if __name__ == '__main__':
    main()
