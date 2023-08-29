'''1. Средний балл, который определенный преподаватель ставит определенному студенту.'''

SELECT s.student_name, t.teacher_name, AVG(g.grade) AS avg_g
	FROM grades AS g
		JOIN courses AS c ON c.id = g.course_id 
			JOIN teachers AS t ON t.id = c.teacher_id
		JOIN students AS s ON s.id = g.student_id
	WHERE s.id = 8 AND t.id = 5
	GROUP BY s.id