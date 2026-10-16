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
    SELECT id, year FROM movie_new WHERE title = '千与千寻'
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
),
scored AS (
    SELECT m.title, m.rating,
           COALESCE(g.g_score, 0) AS gs,
           COALESCE(d.d_score, 0) AS ds,
           COALESCE(c.c_score, 0) AS cs,
           COALESCE(1 / (1 + ABS(m.year - t.year)) *0.005, 0) AS ys
    FROM movie_new m
    CROSS JOIN target t
    LEFT JOIN g ON g.movie_id = m.id
    LEFT JOIN d ON d.movie_id = m.id
    LEFT JOIN c ON c.movie_id = m.id
    WHERE (g.movie_id IS NOT NULL OR d.movie_id IS NOT NULL OR c.movie_id IS NOT NULL) AND m.id <> t.id
)
SELECT title, rating,
       ROUND(gs, 4) AS 类型分,
       ROUND(ds, 4) AS 导演分,
       ROUND(cs, 4) AS 国家分,
       ROUND(ys, 4) AS 年份分
FROM scored
ORDER BY gs + ds + cs + ys DESC, rating DESC
LIMIT 15;