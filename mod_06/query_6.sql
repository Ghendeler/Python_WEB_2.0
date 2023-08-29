'''6. Найти список студентов в определенной группе.'''

SELECT s.student_name, g.groupe_name
	FROM students AS s
	LEFT JOIN groupes AS g ON s.groupe_id = g.id
	WHERE s.groupe_id = 2