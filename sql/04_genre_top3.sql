WITH ranked AS (
    SELECT g.name  AS genre,
       m.title,
       m.rating,
       RANK() OVER (PARTITION BY g.name ORDER BY m.rating DESC) AS       rn
    FROM movie_new m
    JOIN movie_genre mg ON m.id = mg.movie_id
    JOIN genre g        ON mg.genre_id = g.id
)
SELECT *
FROM ranked 
WHERE rn <= 3
ORDER BY genre, rn;
