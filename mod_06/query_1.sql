'''1. Найти 5 студентов с наибольшим средним баллом по всем предметам.'''

SELECT s.student_name, AVG(g.grade) AS avg 
FROM grades AS g
LEFT JOIN students AS s ON g.student_id = s.id
GROUP BY g.student_id 
ORDER BY avg DESC
LIMIT 5