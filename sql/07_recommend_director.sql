WITH genre_cnt AS (
    SELECT genre_id, COUNT(*) AS movie_count
    FROM movie_genre
    GROUP BY genre_id
),
director_cnt AS (
    SELECT director_id, COUNT(*) AS movie_count
    FROM movie_director
    GROUP BY director_id
),
country_cnt AS (
    SELECT country_id, COUNT(*) AS movie_count
    FROM movie_country
    GROUP BY country_id
),
target AS (
    SELECT id FROM movie_new WHERE title = '千与千寻'
),
g AS (
    SELECT b.movie_id, SUM(1 / gc.movie_count) AS g_score
    FROM target t
    JOIN movie_genre a  ON a.movie_id = t.id
    JOIN movie_genre b  ON a.genre_id = b.genre_id AND b.movie_id <> a.movie_id
    JOIN genre_cnt gc   ON gc.genre_id = a.genre_id
    GROUP BY b.movie_id
),
d AS (
    SELECT b.movie_id, SUM(1 / dc.movie_count) AS d_score 
    FROM target t 
    JOIN movie_director a ON a.movie_id = t.id 
    JOIN movie_director b ON a.director_id = b.director_id AND b.movie_id <> a.movie_id
    JOIN director_cnt dc  ON dc.director_id = a.director_id
    GROUP BY b.movie_id
),
c AS (
    SELECT b.movie_id, SUM(1 / cc.movie_count) AS c_score
    FROM target t
    JOIN movie_country a  ON a.movie_id = t.id
    JOIN movie_country b  ON a.country_id = b.country_id AND b.movie_id <> a.movie_id
    JOIN country_cnt cc   ON cc.country_id = a.country_id
    GROUP BY b.movie_id
)
SELECT m.title, m.rating,
       ROUND(COALESCE(g.g_score, 0), 4) AS 类型分,
       ROUND(COALESCE(d.d_score, 0), 4) AS 导演分,
       ROUND(COALESCE(c.c_score, 0), 4) AS 国家分
FROM movie_new m
LEFT JOIN g ON g.movie_id = m.id
LEFT JOIN d ON d.movie_id = m.id
LEFT JOIN c ON c.movie_id = m.id
WHERE g.movie_id IS NOT NULL OR d.movie_id IS NOT NULL
ORDER BY 类型分 + 导演分 + 国家分 DESC, m.rating DESC
LIMIT 15;