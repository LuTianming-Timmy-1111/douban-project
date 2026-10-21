#!/bin/bash
set -e
cd "$(dirname "$0")"

echo "== 1/4 启动数据库 =="
docker-compose up -d db

echo "== 2/4 爬取 =="
docker-compose run --rm spider

echo "== 3/4 拆表 =="
./run_split.sh

echo "== 4/4 检查 =="
./run_check.sh

echo "== 全部完成 =="
