#!/bin/bash
echo "===== 交付质检工具环境初始化 ====="
# 启动mysql
sudo service mysql start
# 初始化数据库
mysql -uroot -p123456 < ./sql/create_table.sql
# 激活python虚拟环境
echo "请手动执行: source venv/bin/activate"
echo "环境部署完成"

