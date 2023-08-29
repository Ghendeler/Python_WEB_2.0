import sqlite3
from datetime import datetime
from random import choice, randint

import faker


NUMBER_STUDENTS = 50
NUMBER_GROUPES = 3
NUMBER_COURSES = 8
NUMBER_TEACHERS = 5
NUMBER_GRADES = 20


def generate_fake_data(number_students, number_teachers,
                       number_courses, number_groupes) -> tuple():
    fake_students = []  # здесь будем хранить студентов
    fake_teachers = []  # здесь будем хранить преподавателей
    fake_courses = []  # здесь будем хранить должности
    fake_groupes = []  # здесь будем хранить группы

    fake_data = faker.Faker('uk_UA')

    # Создадим набор компаний в количестве number_students
    for _ in range(number_students):
        fake_students.append(fake_data.name())

    # Сгенерируем теперь number_teachers количество преподавателей'''
    for _ in range(number_teachers):
        fake_teachers.append(fake_data.name())

    # И number_courses набор курсов
    for _ in range(number_courses):
        fake_courses.append(fake_data.job())

    for _ in range(number_groupes):
        fake_groupes.append(fake_data.bothify(text='??-##', letters='ABCDE'))

    return fake_students, fake_teachers, fake_courses, fake_groupes


def prepare_data(students, teachers, courses, groupes) -> tuple():

    # подготавливаем список кортежей студентов
    for_students = []
    for student in students:
        for_students.append((student, randint(1, NUMBER_GROUPES + 1)))

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
    # есть оценки по предметам с указанием когда оценка получена
    # до 20 оценок у каждого студента по всем предметам
    for_grades = []
    for student_id in range(1, NUMBER_STUDENTS + 1):
        for _ in range(NUMBER_GRADES):
            date = datetime(2023, choice([1, 2, 3, 4, 5]), randint(1, 28)).date()
            for_grades.append((randint(5, 12), student_id,
                               randint(1, NUMBER_COURSES), date))
    for_grades.sort(key=lambda d: d[3])

    return for_students, for_teachers, for_courses, for_groupes, for_grades


def insert_data_to_db(students, teachers, courses, groupes, grades) -> None:

    with sqlite3.connect('university.db') as con:
        cur = con.cursor()

        sql_to_students = """INSERT INTO students(student_name, groupe_id)
                               VALUES (?, ?)"""
        cur.executemany(sql_to_students, students)

        sql_to_teachers = """INSERT INTO teachers(teacher_name)
                               VALUES (?)"""
        cur.executemany(sql_to_teachers, teachers)

        sql_to_courses = """INSERT INTO courses(course_name, teacher_id)
                              VALUES (?, ?)"""
        cur.executemany(sql_to_courses, courses)

        sql_to_groupes = """INSERT INTO groupes(groupe_name)
                              VALUES (?)"""
        cur.executemany(sql_to_groupes, groupes)

        sql_to_grades = """INSERT INTO grades(grade, student_id, course_id, date_of)
                              VALUES (?, ?, ?, ?)"""
        cur.executemany(sql_to_grades, grades)

        con.commit()


def main():
    students, teachers, courses, groupes, grades = prepare_data(
        *generate_fake_data(NUMBER_STUDENTS, NUMBER_TEACHERS,
                            NUMBER_COURSES, NUMBER_GROUPES))

    insert_data_to_db(students, teachers, courses, groupes, grades)


if __name__ == "__main__":
    main()
