'''10.Список курсов, которые определенному студенту 
читает определенный преподаватель.'''

SELECT s.student_name, t.teacher_name, c.course_name
	FROM grades AS g
		JOIN courses AS c ON c.id = g.course_id
			JOIN teachers AS t ON t.id = c.teacher_id 
		JOIN students AS s ON s.id = g.student_id
	WHERE s.id = 42 AND t.id = 5
	GROUP BY g.course_id