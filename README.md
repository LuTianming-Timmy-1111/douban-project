# 豆瓣 Top250 电影爬虫与分析

数据库课程项目：爬取豆瓣电影 Top250，规范化存入 MySQL，并做统计分析。

## 文件说明

- `spider.py`：爬虫，抓取 250 部电影的片名、评分、年份、国家、类型，写入 movie 表
- `split_tables.py`：把 movie 宽表拆成 5 张规范化的表
- `run_split.sh`：加载 .env 后运行拆表脚本
- `docker-compose.yml` / `Dockerfile`：用 Docker 运行 MySQL 和爬虫

## 运行步骤

1. 复制配置文件并填写数据库密码：`cp .env.example .env`
2. 启动数据库：`docker-compose up -d db`
3. 运行爬虫：`docker-compose up spider`
4. 拆表：`./run_split.sh`
