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
cursor.execute("DELETE FROM movie_director")
cursor.execute("DELETE FROM movie_new")
cursor.execute("DELETE FROM genre")
cursor.execute("DELETE FROM country")
cursor.execute("DELETE FROM director")

def get_or_create(table, name):
    cursor.execute(f"SELECT id FROM {table} WHERE name = %s", (name,))
    row = cursor.fetchone()
    if row:
        return row[0]
    
    cursor.execute(f"INSERT INTO {table} (name) VALUES (%s)", (name,))
    return cursor.lastrowid

def split_name(name):
    ch = name[0]
    if '\u4e00' <= ch <= '\u9fff':
        parts = name.split(' ', 1)
        cn = parts[0].strip()
        en = parts[1].strip() if len(parts) > 1 else None
    else:
        cn = None
        en = name.strip()
    return (cn, en)

def get_or_create_director(cn, en):
    cursor.execute(
        "SELECT id, name_cn, name_en FROM director WHERE name_cn = %s OR name_en = %s",
        (cn, en)
    )
    rows = cursor.fetchall()

    if len(rows) > 1:
        print('⚠ 导演匹配到多条记录：', cn, en, rows)

    if rows:
        did, old_cn, old_en = rows[0]
        #中文名
        if old_cn is None and cn is not None:
            cursor.execute("UPDATE director SET name_cn = %s WHERE id = %s", (cn, did))
        elif old_cn is not None and cn is not None and old_cn != cn:
            print('⚠ 导演中文名不一致：', old_cn, cn)
        #英文名
        if old_en is None and en is not None:
            cursor.execute("UPDATE director SET name_en = %s WHERE id = %s", (en, did))
        elif old_en is not None and en is not None and old_en != en:
            print('⚠ 导演英文名不一致：', old_en, en)
        return did

    cursor.execute(
        "INSERT INTO director (name_cn, name_en) VALUES (%s, %s)",
        (cn, en)
    )
    return cursor.lastrowid

cursor.execute("SELECT title, rating, year, country, genre, director FROM movie")
movies = cursor.fetchall()

for title, rating, year, country_str, genre_str, director_str in movies:
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
    if director_str:
        for name in [d.strip() for d in director_str.split('/') if d.strip()]:
            cn, en = split_name(name)
            director_id = get_or_create_director(cn, en)
            cursor.execute(
                "INSERT IGNORE INTO movie_director (movie_id, director_id) VALUES (%s, %s)", 
                (movie_id, director_id)
            )

conn.commit()
cursor.close()
conn.close()
print('拆表完成! ')
