'''9. Найти список курсов, которые посещает определенный студент.'''

SELECT s.student_name, c.course_name
	FROM grades AS g
        JOIN students AS s ON s.id = g.student_id
        JOIN courses AS c ON c.id = g.course_id
	WHERE s.id = 41
	GROUP BY g.course_id
