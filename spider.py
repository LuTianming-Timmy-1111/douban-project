import os
import requests
from bs4 import BeautifulSoup
import pymysql
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# ===== 连接数据库、建表（表结构升级为5个字段）=====
for i in range(10):
    try:
        conn = pymysql.connect(
            host='db', port=3306,
            user='root', password=os.environ['DB_PASSWORD'],
            charset='utf8mb4'
        )
        break
    except pymysql.err.OperationalError:
        print(f'数据库还没就绪, 3 秒后重试 (第 {i + 1} 次) ')
        time.sleep(3)
else:
    raise SystemExit('数据库一直连不上, 放弃')
    
cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS douban")
cursor.execute("USE douban")
# 先删旧表重建（字段变了）
cursor.execute("DROP TABLE IF EXISTS movie")
cursor.execute("""
    CREATE TABLE movie (
        id INT PRIMARY KEY AUTO_INCREMENT,
        title VARCHAR(100),
        rating DECIMAL(3,1),
        year VARCHAR(10),
        country VARCHAR(100),
        genre VARCHAR(100)
    )
""")

# ===== 爬10页 =====
for start in range(0, 250, 25):
    url = f'https://movie.douban.com/top250?start={start}'
    print(f'--- 正在爬第 {start // 25 + 1} 页 ---')

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    items = soup.find_all('div', class_='item')
    for item in items:
        title = item.find('span', class_='title').text
        rating = item.find('span', class_='rating_num').text

        # 解析 bd 文本，切出 年份/国家/类型
        bd = item.find('div', class_='bd').find('p').text
        bd = bd.replace('\xa0', ' ')
        lines = [line.strip() for line in bd.split('\n') if line.strip()]
        info_line = lines[1]
        parts = info_line.split('/')

        # 健壮性处理：不够3块就填默认值，避免越界报错
        year = parts[0].strip()[:4] if len(parts) > 0 else ''
        country = parts[-2].strip() if len(parts) > 2 else ''
        genre = parts[-1].strip() if len(parts) > 2 else ''
        
        if len(parts) < 3:
            print('⚠ 格式异常，已留空：', title, repr(info_line))
        
        # 插入5个字段
        cursor.execute(
            "INSERT INTO movie (title, rating, year, country, genre) VALUES (%s, %s, %s, %s, %s)",
            (title, rating, year, country, genre)
        )
        print(title, rating, year, country, genre)

    time.sleep(2)

conn.commit()
cursor.close()
conn.close()
print('全部250部电影（含详细字段）已存入数据库！')
