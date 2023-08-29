'''4. Найти средний балл на потоке (по всей таблице оценок).'''

SELECT  grp.groupe_name, AVG(g.grade) AS avg_g
	FROM grades AS g
		JOIN students AS s ON s.id = g.student_id
			JOIN groupes AS grp ON grp.id = g.course_id
	GROUP BY g.course_id