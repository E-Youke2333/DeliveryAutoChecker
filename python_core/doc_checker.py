#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import logging
from datetime import datetime
from mysql.connector import connect, Error

class Config:
    """配置管理类"""
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        # 检查配置文件是否存在
        if not os.path.exists(self.config_file):
            if os.path.exists('config.json.example'):
                print(f"⚠️  配置文件 {self.config_file} 不存在")
                print(f"请复制 config.json.example 为 {self.config_file} 并填写配置")
                print(f"命令: cp config.json.example config.json")
                sys.exit(1)
            else:
                print(f"❌ 配置文件 {self.config_file} 不存在")
                print(f"请创建配置文件或从模板复制")
                sys.exit(1)
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ 配置文件格式错误: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ 读取配置文件失败: {e}")
            sys.exit(1)
    
    def get_db_config(self):
        """获取数据库配置"""
        db_config = self.config.get('database', {})
        # 设置默认值
        return {
            'host': db_config.get('host', 'localhost'),
            'port': db_config.get('port', 3306),
            'user': db_config.get('user', 'root'),
            'password': db_config.get('password', ''),
            'database': db_config.get('database', 'delivery_quality'),
            'charset': db_config.get('charset', 'utf8mb4')
        }
    
    def get_app_config(self):
        """获取应用配置"""
        app_config = self.config.get('app', {})
        return {
            'test_folder': app_config.get('test_folder', './test_file'),
            'log_level': app_config.get('log_level', 'INFO'),
            'supported_extensions': app_config.get('supported_extensions', ['.md', '.docx']),
            'required_keywords': app_config.get('required_keywords', ['交付说明书'])
        }
    
    def get_logging_config(self):
        """获取日志配置"""
        return self.config.get('logging', {})
    
    def get_scan_config(self):
        """获取扫描配置"""
        return self.config.get('scan', {})

class DocChecker:
    """文档校验器"""
    def __init__(self, config):
        self.config = config
        self.db_config = config.get_db_config()
        self.app_config = config.get_app_config()
        self.scan_config = config.get_scan_config()
        
    def test_db_connection(self):
        """测试数据库连接"""
        try:
            conn = connect(**self.db_config)
            conn.close()
            return True
        except Error as e:
            print(f"❌ 数据库连接失败: {e}")
            print(f"   Host: {self.db_config['host']}")
            print(f"   User: {self.db_config['user']}")
            print(f"   Database: {self.db_config['database']}")
            return False
    
    def scan_documents(self):
        """扫描并校验文档"""
        folder_path = self.app_config['test_folder']
        required_keywords = self.app_config['required_keywords']
        supported_extensions = self.app_config['supported_extensions']
        exclude_patterns = self.scan_config.get('exclude_patterns', [])
        max_size_mb = self.scan_config.get('max_file_size_mb', 50)
        
        # 检查文件夹
        if not os.path.exists(folder_path):
            print(f"📁 创建测试文件夹: {folder_path}")
            os.makedirs(folder_path)
            print(f"请将测试文档放入 {folder_path} 目录")
            return 0
        
        # 扫描文件
        files = os.listdir(folder_path)
        if not files:
            print(f"📁 文件夹 {folder_path} 为空")
            print(f"请添加测试文档到 {folder_path} 目录")
            print(f"支持的文件格式: {', '.join(supported_extensions)}")
            return 0
        
        error_count = 0
        total_files = 0
        error_list = []
        
        print(f"\n📂 扫描目录: {folder_path}")
        print(f"📋 校验规则: 文件名必须包含 '{' 或 '.join(required_keywords)}'")
        print("-" * 60)
        
        for file in files:
            # 检查是否应该排除
            should_exclude = False
            for pattern in exclude_patterns:
                if pattern in file:
                    should_exclude = True
                    break
            if should_exclude:
                continue
            
            # 检查文件扩展名
            ext = os.path.splitext(file)[1].lower()
            if ext not in supported_extensions:
                continue
            
            total_files += 1
            
            # 检查文件大小
            file_path = os.path.join(folder_path, file)
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
            if file_size > max_size_mb:
                print(f"⚠️  {file} - 文件过大 ({file_size:.1f}MB)，跳过")
                continue
            
            # 校验文件名是否包含关键词
            has_keyword = any(keyword in file for keyword in required_keywords)
            
            if not has_keyword:
                error_count += 1
                error_list.append(file)
                print(f"❌ {file} - 缺少标准命名")
            else:
                print(f"✅ {file} - 通过")
        
        print("-" * 60)
        
        # 输出统计
        print(f"\n📊 扫描统计:")
        print(f"   总文件数: {total_files}")
        print(f"   异常文件: {error_count}")
        print(f"   通过文件: {total_files - error_count}")
        
        if error_list:
            print(f"\n❌ 异常文件列表:")
            for f in error_list:
                print(f"   - {f}")
        
        return error_count
    
    def write_log_to_db(self, error_count, total_files):
        """写入日志到数据库"""
        if not self.config.get_logging_config().get('enable_db_log', True):
            print("ℹ️  数据库日志记录已禁用")
            return
        
        try:
            conn = connect(**self.db_config)
            cursor = conn.cursor()
            
            # 检查表是否存在
            cursor.execute("SHOW TABLES LIKE 'doc_check_log'")
            if not cursor.fetchone():
                print("⚠️  表 doc_check_log 不存在，请先执行 sql/create_table.sql")
                conn.close()
                return
            
            # 写入日志
            insert_sql = """
                INSERT INTO doc_check_log(file_name, error_count, check_time) 
                VALUES(%s, %s, %s)
            """
            check_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute(insert_sql, (f"扫描_{total_files}个文件", error_count, check_time))
            conn.commit()
            conn.close()
            
            print(f"✅ 校验日志已写入数据库")
        except Error as e:
            print(f"❌ 数据库写入失败: {e}")
            print(f"   请检查数据库配置和连接")

def main():
    """主函数"""
    print("=" * 60)
    print("📋 交付自动化质检工具 v1.0")
    print("=" * 60)
    
    # 加载配置
    config = Config()
    
    # 显示当前配置
    db_config = config.get_db_config()
    print(f"\n📌 数据库配置:")
    print(f"   Host: {db_config['host']}:{db_config['port']}")
    print(f"   User: {db_config['user']}")
    print(f"   Database: {db_config['database']}")
    
    # 创建校验器
    checker = DocChecker(config)
    
    # 测试数据库连接
    if not checker.test_db_connection():
        print("\n⚠️  数据库连接失败，将跳过数据库日志记录")
        print("   请检查 config.json 中的数据库配置")
    
    # 执行扫描
    error_count = checker.scan_documents()
    
    # 写入日志
    if checker.test_db_connection():
        checker.write_log_to_db(error_count, len(os.listdir(checker.app_config['test_folder'])))
    
    print("\n" + "=" * 60)
    print(f"✅ 校验完成，总异常文件数：{error_count}")
    print("=" * 60)

if __name__ == "__main__":
    main()
