SELECT COUNT(*)                           AS total_rows,
       COUNT(DISTINCT movie_id)           AS movie_cnt,
       ROUND(COUNT(*) / COUNT(DISTINCT movie_id), 2) AS avg_genres
FROM movie_genre;