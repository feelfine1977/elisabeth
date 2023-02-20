-- SQLite
SELECT case_id, COUNT(*) AS 'Number of Events'
FROM eventlog 
GROUP BY case_id
ORDER BY COUNT(*) DESC
LIMIT 1