WITH genre_cnt AS (
    SELECT mg.genre_id, 
           COUNT(*) AS movie_count
    FROM movie_genre mg
    GROUP BY mg.genre_id
)
SELECT m2.title, 
       m2.rating, 
       COUNT(*) AS shared, 
       ROUND(SUM(1 / gc.movie_count), 4) AS score 
FROM movie_new m1
JOIN movie_genre a  ON m1.id = a.movie_id
JOIN movie_genre b  ON a.genre_id = b.genre_id
                   AND a.movie_id <> b.movie_id
JOIN movie_new m2   ON b.movie_id = m2.id
JOIN genre_cnt gc   ON a.genre_id = gc.genre_id
WHERE m1.title = '千与千寻'
GROUP BY m2.id, m2.title, m2.rating
ORDER BY score DESC, m2.rating DESC
LIMIT 10;