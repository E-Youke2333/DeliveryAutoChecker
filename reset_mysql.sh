#!/bin/bash
echo "=== 重置MySQL Root密码 ==="

# 清理进程
echo "1. 清理MySQL进程..."
sudo pkill -9 mysqld 2>/dev/null
sudo pkill -9 mysqld_safe 2>/dev/null
sleep 2

# 创建目录
echo "2. 创建运行目录..."
sudo mkdir -p /var/run/mysqld
sudo chown mysql:mysql /var/run/mysqld

# 安全模式启动
echo "3. 启动MySQL安全模式..."
sudo mysqld_safe --skip-grant-tables --skip-networking &
sleep 5

# 重置密码
echo "4. 重置root密码..."
sudo mysql -uroot << EOF
FLUSH PRIVILEGES;
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '123456';
FLUSH PRIVILEGES;
EOF

# 停止安全模式
echo "5. 停止安全模式..."
sudo pkill -9 mysqld
sudo pkill -9 mysqld_safe
sleep 3

# 正常启动
echo "6. 正常启动MySQL..."
sudo systemctl start mysql

# 测试连接
echo "7. 测试连接..."
if mysql -uroot -p123456 -e "SELECT 1" >/dev/null 2>&1; then
    echo "✅ MySQL重置成功！"
    echo "现在可以运行: python3 python_core/doc_checker.py"
else
    echo "❌ 连接失败，请检查日志"
    sudo tail -20 /var/log/mysql/error.log
fi
