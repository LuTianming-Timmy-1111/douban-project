#!/bin/bash
# 导出规范化表的结构到 schema.sql
# 不含数据、不含 movie 表（其结构由 spider.py 定义）、去掉 AUTO_INCREMENT
set -o pipefail

docker exec douban-project-db-1 sh -c 'mysqldump -uroot -p"$MYSQL_ROOT_PASSWORD" --no-data --skip-add-drop-table --skip-dump-date --ignore-table=douban.movie douban' \
  | sed 's/ AUTO_INCREMENT=[0-9]*//' > schema.tmp \
  && mv schema.tmp schema.sql \
  && echo "schema.sql 已更新"
