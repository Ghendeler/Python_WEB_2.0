'''3. Найти средний балл в группах по определенному предмету.'''

SELECT c.course_name, grp.groupe_name, AVG(g.grade) AS avg_g
	FROM grades AS g
		JOIN courses AS c ON c.id = g.course_id 
		JOIN students AS s ON s.id = g.student_id
			JOIN groupes AS grp ON grp.id = s.groupe_id
	WHERE c.id = 4
	GROUP BY grp.id