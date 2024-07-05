import random
import time

import pymysql

# 数据库连接参数

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '3074272950',
    'db': 'student',
}

# 初始计数器
count = 0

# 连接到数据库
connection = pymysql.connect(**db_config)

try:
    while count < 2:  # 只执行两次获取人名的操作
        with connection.cursor() as cursor:
            # 从数据库student中的表student_info获取数据
            sql = "SELECT id, name FROM student_info ORDER BY RAND() LIMIT 1"

            cursor.execute(sql)
            results = cursor.fetchall()

            # 获取随机人名
            if results:
                count += 1
                print(f"\n第{count}次随机抽签")
                # 打印获取的人名
                for (id, name) in results:
                    print("随机演讲的幸运儿是:", id, name)
                    # 获取当前系统时间
                    current_time = time.strftime("%Y年%m月%d日 %H:%M:%S", time.localtime())
                    print(current_time)
            else:
                print("没有获取到人名")
                break

finally:
    # 关闭数据库连接
    connection.close()
# 打印总共进行了多少次随机抽签
print(f"\n总共执行了{count}次随机抽签")
