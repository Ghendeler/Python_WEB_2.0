'''7. Найти оценки студентов в отдельной группе по определенному предмету.'''

SELECT grp.groupe_name, c.course_name, s.student_name, g.grade
	FROM grades AS g
		JOIN courses AS c
		JOIN students AS s ON s.id = g.student_id
			JOIN groupes AS grp ON grp.id = g.course_id
	WHERE c.id = 6 AND grp.id = 2