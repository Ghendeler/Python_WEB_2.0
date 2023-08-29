'''8. Найти средний балл, который ставит определенный 
преподаватель по своим предметам.'''

SELECT avg(g.grade) AS avg_gr, c.course_name, t.teacher_name
	FROM grades AS g
        JOIN courses AS c ON c.id = g.course_id
        JOIN teachers AS t ON t.id = c.teacher_id
	WHERE t.id = 2
	GROUP BY g.course_id