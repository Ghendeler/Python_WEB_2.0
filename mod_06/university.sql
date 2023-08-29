-- Table: students
DROP TABLE IF EXISTS students;
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name VARCHAR(255) UNIQUE NOT NULL,
    groupe_id INTEGER,
    FOREIGN KEY (groupe_id) REFERENCES groupes (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);

-- Table: groupes
DROP TABLE IF EXISTS groupes;
CREATE TABLE groupes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    groupe_name VARCHAR(255) UNIQUE NOT NULL
);

-- Table: teachers
DROP TABLE IF EXISTS teachers;
CREATE TABLE teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    teacher_name VARCHAR(255) UNIQUE NOT NULL
);

-- Table: courses
DROP TABLE IF EXISTS courses;
CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name VARCHAR(255) UNIQUE NOT NULL,
    teacher_id INTEGER,
    FOREIGN KEY (teacher_id) REFERENCES teachers (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);


-- Table: grades
DROP TABLE IF EXISTS grades;
CREATE TABLE grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    grade INTEGER,
    student_id INTEGER,
    course_id INTEGER,
    date_of DATE NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);
