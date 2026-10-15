SELECT g.name AS genre,
       COUNT(*)                AS movie_count,
       ROUND(AVG(m.rating), 2) AS avg_rating
FROM movie_new m
JOIN movie_genre mg ON m.id = mg.movie_id
JOIN genre g        ON mg.genre_id = g.id
GROUP BY g.name
ORDER BY movie_count DESC;
