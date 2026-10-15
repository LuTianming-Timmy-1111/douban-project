SELECT m2.title, m2.rating, COUNT(*) AS shared_genre_count
FROM movie_new m1
JOIN movie_genre a ON m1.id = a.movie_id
JOIN movie_genre b ON a.genre_id = b.genre_id
                  AND a.movie_id <> b.movie_id
JOIN movie_new m2 ON b.movie_id = m2.id
WHERE m1.title = '千与千寻'
GROUP BY m2.id, m2.title, m2.rating
ORDER BY COUNT(*) DESC, m2.rating DESC
LIMIT 10;