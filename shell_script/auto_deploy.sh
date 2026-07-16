#!/bin/bash
echo "===== 交付质检工具环境初始化 ====="

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查配置文件
check_config() {
    if [ ! -f "config.json" ]; then
        echo -e "${YELLOW}⚠️  配置文件 config.json 不存在${NC}"
        if [ -f "config.json.example" ]; then
            echo "正在从模板创建配置文件..."
            cp config.json.example config.json
            echo -e "${GREEN}✅ 已创建 config.json${NC}"
            echo ""
            echo -e "${YELLOW}请编辑 config.json 填写数据库配置:${NC}"
            echo "   vim config.json"
            echo ""
            echo "必须修改的字段:"
            echo "   - database.password: 你的MySQL密码"
            echo "   - database.user: MySQL用户名 (默认: root)"
            echo "   - database.host: MySQL主机 (默认: localhost)"
            echo "   - database.database: 数据库名 (默认: delivery_quality)"
            echo ""
            echo "可选配置:"
            echo "   - app.required_keywords: 校验关键词列表"
            echo "   - app.supported_extensions: 支持的文件扩展名"
            echo ""
            read -p "修改完成后按回车继续，或按 Ctrl+C 退出..."
        else
            echo -e "${RED}❌ 找不到 config.json.example 模板文件${NC}"
            exit 1
        fi
    fi
}

# 提取数据库配置
get_db_config() {
    DB_HOST=$(python3 -c "import json; print(json.load(open('config.json'))['database'].get('host', 'localhost'))" 2>/dev/null)
    DB_PORT=$(python3 -c "import json; print(json.load(open('config.json'))['database'].get('port', 3306))" 2>/dev/null)
    DB_USER=$(python3 -c "import json; print(json.load(open('config.json'))['database'].get('user', 'root'))" 2>/dev/null)
    DB_PASS=$(python3 -c "import json; print(json.load(open('config.json'))['database'].get('password', ''))" 2>/dev/null)
    DB_NAME=$(python3 -c "import json; print(json.load(open('config.json'))['database'].get('database', 'delivery_quality'))" 2>/dev/null)
    
    if [ -z "$DB_USER" ] || [ -z "$DB_PASS" ] || [ -z "$DB_NAME" ]; then
        echo -e "${RED}❌ 读取配置文件失败，请检查 config.json 格式${NC}"
        echo "请确保 JSON 格式正确，可以使用 python3 -m json.tool config.json 验证"
        exit 1
    fi
}

# 测试数据库连接
test_connection() {
    echo "测试数据库连接..."
    mysql -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" -p"$DB_PASS" -e "SELECT 1" >/dev/null 2>&1
    return $?
}

# 主流程
main() {
    # 1. 检查配置
    check_config
    
    # 2. 读取配置
    echo -e "\n${GREEN}📌 读取配置...${NC}"
    get_db_config
    echo "   Host: $DB_HOST:$DB_PORT"
    echo "   User: $DB_USER"
    echo "   Database: $DB_NAME"
    
    # 3. 启动MySQL
    echo -e "\n${GREEN}🚀 启动 MySQL 服务...${NC}"
    sudo service mysql start 2>/dev/null || sudo systemctl start mysql 2>/dev/null
    
    # 4. 测试连接
    if test_connection; then
        echo -e "${GREEN}✅ 数据库连接成功${NC}"
    else
        echo -e "${RED}❌ 数据库连接失败${NC}"
        echo "请检查:"
        echo "   1. MySQL是否已启动: sudo service mysql status"
        echo "   2. config.json 中的配置是否正确"
        echo "   3. 密码是否正确"
        exit 1
    fi
    
    # 5. 创建数据库
    echo -e "\n${GREEN}📊 创建数据库...${NC}"
    mysql -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" -p"$DB_PASS" -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ 数据库创建成功${NC}"
    else
        echo -e "${RED}❌ 数据库创建失败${NC}"
        exit 1
    fi
    
    # 6. 导入表结构
    echo -e "\n${GREEN}📋 导入表结构...${NC}"
    mysql -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" < ./sql/create_table.sql 2>/dev/null
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ 表结构导入成功${NC}"
    else
        echo -e "${RED}❌ 表结构导入失败${NC}"
        exit 1
    fi
    
    echo -e "\n${GREEN}===== 部署完成 =====${NC}"
    echo ""
    echo "下一步:"
    echo "1. source venv/bin/activate"
    echo "2. python3 python_core/doc_checker.py"
    echo ""
    echo "配置说明:"
    echo "   - 修改 config.json 可调整校验规则"
    echo "   - 支持自定义关键词、文件类型等"
}

# 执行
main
