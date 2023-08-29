'''2. Найти студента с наивысшим средним баллом по определенному предмету.'''

SELECT s.student_name, AVG(g.grade) AS avg 
FROM grades AS g
LEFT JOIN students AS s ON g.student_id = s.id
WHERE g.course_id = 1
GROUP BY g.student_id 
ORDER BY avg DESC
LIMIT 1