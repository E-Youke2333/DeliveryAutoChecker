# DeliveryAutoChecker - 交付自动化质检工具

## 项目简介
自动化质检工具，用于检查交付文档的规范性，并将校验结果存储到 MySQL 数据库。

## 特性
- 灵活配置：通过 JSON 配置文件管理所有参数
- 数据库支持：自动记录校验日志到 MySQL
- 多格式支持：支持 .md、.docx、.txt 等格式
- 自定义规则：可配置关键词、排除模式、文件大小限制
- 安全可靠：密码等敏感信息通过配置文件管理

## 快速开始
### 环境要求
- Ubuntu 20.04+ / WSL2
- Python 3.8+
- MySQL 8.0+

### 安装步骤
#### 1. 克隆项目
\`\`\`bash
git clone git@github.com:E-Youke2333/DeliveryAutoChecker.git
cd DeliveryAutoChecker
\`\`\`

#### 2. 创建虚拟环境
\`\`\`bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
\`\`\`

#### 3. 配置数据库
\`\`\`bash
cp config.json.example config.json
vim config.json
\`\`\`

#### 4. 初始化数据库
\`\`\`bash
chmod +x shell_script/auto_deploy.sh
./shell_script/auto_deploy.sh
\`\`\`

#### 5. 运行质检
\`\`\`bash
python3 python_core/doc_checker.py
\`\`\`

## 目录结构
\`\`\`
DeliveryAutoChecker/
├── python_core/
│   └── doc_checker.py
├── shell_script/
│   └── auto_deploy.sh
├── perl_script/
│   └── log_filter.pl
├── sql/
│   └── create_table.sql
├── test_file/
├── logs/
├── config.json.example
├── config.json
├── requirements.txt
└── README.md
\`\`\`

## 配置说明
### config.json 完整配置
\`\`\`json
{
    "database": {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "your_password_here",
        "database": "delivery_quality",
        "charset": "utf8mb4"
    },
    "app": {
        "test_folder": "./test_file",
        "log_level": "INFO",
        "supported_extensions": [".md", ".docx", ".txt"],
        "required_keywords": ["交付说明书", "验收报告", "测试报告"]
    },
    "logging": {
        "enable_db_log": true,
        "enable_file_log": false,
        "log_file": "./logs/checker.log",
        "max_log_size_mb": 10
    },
    "scan": {
        "recursive": false,
        "exclude_patterns": ["~$", ".tmp", ".bak"],
        "max_file_size_mb": 50
    }
}
\`\`\`

### 配置字段说明
| 字段 | 说明 | 默认值 |
|------|------|--------|
| database.host | MySQL 主机地址 | localhost |
| database.port | MySQL 端口 | 3306 |
| database.user | MySQL 用户名 | root |
| database.password | MySQL 密码 | 必须修改 |
| database.database | 数据库名称 | delivery_quality |
| app.supported_extensions | 支持的文件扩展名 | [".md", ".docx"] |
| app.required_keywords | 校验关键词列表 | ["交付说明书"] |
| scan.max_file_size_mb | 最大文件大小(MB) | 50 |

## 数据库结构
数据库名：delivery_quality

### fault_ticket - ITR故障工单表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 工单ID (主键) |
| device_model | VARCHAR(100) | 设备型号 |
| fault_desc | TEXT | 故障描述 |
| deliver_date | DATE | 交付日期 |
| status | TINYINT | 状态 (0未解决/1已闭环) |
| create_time | DATETIME | 创建时间 |

### doc_check_log - 文档校验日志表
| 字段 | 类型 | 说明 |
|------|------|------|
| log_id | INT | 日志ID (主键) |
| file_name | VARCHAR(200) | 文件名 |
| error_count | INT | 异常数量 |
| check_time | DATETIME | 校验时间 |

## 技术栈
- Python 3.8+
- MySQL 8.0
- mysql-connector-python
- Shell Script
- Perl
