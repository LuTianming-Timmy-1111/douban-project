import os
import sys

import pymysql

CHECKS = [
    ("电影总数应为 250",
     "SELECT COUNT(*) AS n FROM movie_new HAVING n <> 250"),
    ("片名为空",
     "SELECT id, title FROM movie_new WHERE title IS NULL OR title = ''"),
    ("评分为空或超出 0-10",
     "SELECT id, title, rating FROM movie_new "
     "WHERE rating IS NULL OR rating NOT BETWEEN 0 AND 10"),
    ("年份不是 4 位数字",
     "SELECT id, title, `year` FROM movie_new "
     "WHERE `year` IS NULL OR `year` NOT REGEXP '^[0-9]{4}$'"),
    ("没有类型的电影",
     "SELECT m.id, m.title FROM movie_new m "
     "LEFT JOIN movie_genre mg ON m.id = mg.movie_id "
     "WHERE mg.movie_id IS NULL"),
    ("没有国家的电影",
     "SELECT m.id, m.title FROM movie_new m "
     "LEFT JOIN movie_country mc ON m.id = mc.movie_id "
     "WHERE mc.movie_id IS NULL"),
    ("没有导演的电影",
     "SELECT m.id, m.title FROM movie_new m "
     "LEFT JOIN movie_director md ON m.id = md.movie_id "
     "WHERE md.movie_id IS NULL"),
]

conn = pymysql.connect(
    host='localhost',
    port=3307,
    user='root',
    password=os.environ['MYSQL_ROOT_PASSWORD'],
    database='douban',
    charset='utf8mb4'
)
cur = conn.cursor()

failed = 0
for name, sql in CHECKS:
    cur.execute(sql)
    rows = cur.fetchall()
    if rows:
        failed += 1
        print("✗", name, len(rows), "行")
        for row in rows[:5]:
            print("   ", row)
    else:
        print("✓", name)

cur.close()
conn.close()

print(len(CHECKS) - failed, "/", len(CHECKS), "项通过")
sys.exit(1 if failed else 0)
