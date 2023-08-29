'''5. Найти какие курсы читает определенный преподаватель.'''

SELECT c.course_name, t.teacher_name
	FROM courses AS c
	LEFT JOIN teachers AS t ON c.teacher_id = t.id
	WHERE c.teacher_id = 2