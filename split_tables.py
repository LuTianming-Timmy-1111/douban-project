import os
import pymysql

conn = pymysql.connect(
    host='localhost',
    port=3307,
    user='root',
    password=os.environ['MYSQL_ROOT_PASSWORD'],
    database='douban',
    charset='utf8mb4'
)

cursor=conn.cursor()

cursor.execute("DELETE FROM movie_genre")
cursor.execute("DELETE FROM movie_country")
cursor.execute("DELETE FROM movie_new")
cursor.execute("DELETE FROM genre")
cursor.execute("DELETE FROM country")

def get_or_create(table, name):
    cursor.execute(f"SELECT id FROM {table} WHERE name = %s", (name,))
    row = cursor.fetchone()
    if row:
        return row[0]
    
    cursor.execute(f"INSERT INTO {table} (name) VALUES (%s)", (name,))
    return cursor.lastrowid

cursor.execute("SELECT title, rating, year, country, genre FROM movie")
movies = cursor.fetchall()

for title, rating, year, country_str, genre_str in movies:
    cursor.execute(
        "INSERT INTO movie_new (title, rating, year) VALUES (%s, %s, %s)",
        (title, rating, year)
    )
    movie_id = cursor.lastrowid

    if genre_str:
        for g in genre_str.split():
            genre_id = get_or_create('genre', g)
            cursor.execute(
                "INSERT IGNORE INTO movie_genre (movie_id, genre_id) VALUES (%s, %s)",
                (movie_id, genre_id)
            )

    if country_str:
        for c in country_str.split():
            country_id = get_or_create('country', c)
            cursor.execute(
                "INSERT IGNORE INTO movie_country (movie_id, country_id) VALUES (%s, %s)",
                (movie_id, country_id)
            )

conn.commit()
cursor.close()
conn.close()
print('拆表完成! ')
