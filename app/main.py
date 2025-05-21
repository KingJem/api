import os
import sys
import time
import tkinter as tk
from datetime import datetime
from tkinter import messagebox

import pymssql
import requests
## config logger
from loguru import logger

root = tk.Tk()
root.withdraw()

root.geometry("1920x1080")


# 创建日志目录（如果不存在）
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)


# 配置日志文件路径（按日期命名）
def get_log_filename():
    """生成按日期命名的日志文件名"""
    today = datetime.now().strftime("%Y-%m-%d")
    return f"{log_dir}/app_{today}.log"


# 移除默认控制台输出
logger.remove()

# 添加文件处理器，每日生成新文件，保留30天历史
logger.add(
    sink=get_log_filename(),
    level="INFO",
    rotation="00:00",  # 每天午夜创建新文件
    retention="90 days",  # 保留30天的日志
    compression="zip",  # 归档时压缩为zip
    enqueue=True,  # 异步写入
    backtrace=True,  # 异常回溯
    diagnose=True  # 异常诊断信息
)

auth = {
    "user": os.getenv('SQL_USER') or 'sa',
    "password": os.getenv('SQL_PASSWORD') or 'YourStrong!Passw0rd',
    "database": os.getenv('SQL_DATABASE') or 'TestDB',
    "host": os.getenv('SQL_HOST') or 'localhost',
    "port": os.getenv('SQL_PORT') or '1433',
}


# Database configuration
def get_db_connection():
    try:
        return pymssql.connect(**auth)
    except pymssql.Error as e:  # 修改异常类型
        logger.error(f"Connection failed: {str(e)}")
        raise


def get_data(sql_query):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(as_dict=True)
        cursor.execute(sql_query)
        results = [row for row in cursor.fetchall()]
        return {"success": results}
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        return
    finally:
        if conn:
            conn.close()


def post_data(data):
    messagebox.showinfo('info', "正在上传数据")
    response = requests.post("https://httpbin.org/post", data=data)
    logger.info(f"post data: {data} response: {response.json()}")
    return response.json()


def main():
    start = time.time()
    messagebox.showinfo('info', "程序开始运行")
    sql_query = "SELECT * FROM testName"
    result = get_data(sql_query)
    if result:
        logger.info(f"sql query: {sql_query} result: {result}")
        post_data(result)
        spend = time.time() - start
        logger.info(f"time spend: {int(spend)} seconds")

    else:
        messagebox.showerror("连接失败，正在退出")
        root.destroy()
        sys.exit()


if __name__ == '__main__':
    main()
