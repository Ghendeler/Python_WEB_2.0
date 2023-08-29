'''2. Оценки студентов в определенной группе по определенному предмету
    на последнем занятии.'''

SELECT c.course_name, grp.groupe_name, s.student_name, g.grade, g.date_of
	FROM grades AS g
		JOIN courses AS c ON c.id = g.course_id 
		JOIN students AS s ON s.id = g.student_id
			JOIN groupes AS grp ON grp.id = s.groupe_id
	WHERE grp.id = 1 AND c.id = 4 AND g.date_of = (
		SELECT MAX(g.date_of)
			FROM grades AS g
				JOIN courses AS c ON c.id = g.course_id 
				JOIN students AS s ON s.id = g.student_id
					JOIN groupes AS grp ON grp.id = s.groupe_id
			WHERE grp.id = 1 AND c.id = 4
		);