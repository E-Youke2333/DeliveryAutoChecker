import os
from mysql.connector import connect, Error

# 数据库配置
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "delivery_quality"
}

def scan_docs(folder_path="./test_file"):
    error_total = 0
    file_list = os.listdir(folder_path)
    for file in file_list:
        if file.endswith((".md", ".docx")):
            # 模拟校验：判断文件名是否包含必填标识
            if "交付说明书" not in file:
                error_total += 1
                print(f"【异常文档】{file} 缺少标准命名")
    # 写入校验日志
    try:
        conn = connect(**DB_CONFIG)
        cursor = conn.cursor()
        insert_sql = "INSERT INTO doc_check_log(file_name, error_count) VALUES(%s, %s)"
        cursor.execute(insert_sql, ("批量文件扫描", error_total))
        conn.commit()
    except Error as e:
        print("数据库写入失败", e)
    print(f"校验完成，总异常文件数：{error_total}")

if __name__ == "__main__":
    scan_docs()

