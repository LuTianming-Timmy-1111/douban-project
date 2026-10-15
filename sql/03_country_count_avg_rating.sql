SELECT c.name AS country,
       COUNT(*) AS country_count,
       ROUND(AVG(m.rating), 2) AS avg_rating
FROM movie_new m
JOIN movie_country mc ON m.id = mc.movie_id
JOIN country c ON mc.country_id = c.id
GROUP BY c.name
HAVING COUNT(*) >= 5
ORDER BY avg_rating DESC;
