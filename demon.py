import pandas as pd
import pymysql

# 先建立与数据库的连接
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '3074272950',
    'database': 'student'
}

con = pymysql.connect(**db_config)
cursor = con.cursor()

# 创建表
cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INT AUTO_INCREMENT PRIMARY KEY,
    grade TEXT NOT NULL,
    name TEXT NOT NULL,
    is_selected INT NOT NULL
)
""")


# con.connect() 这一行是不必要的，因为pymysql.connect()已经建立了连接

# 用函数从Excel表格中导入数据
def import_from_excel(excel_file):
    # 读取Excel文件
    df = pd.read_excel(excel_file, engine='openpyxl')

    print(df)
    # 假设数据在'Students'sheet上，
    # if 'Students' not in df.columns:
    #     raise ValueError("Excel file does not contain 'Students' sheet or column names are different.")

    # 将dataframe转换为列表元组，准备插入数据库
    data_to_insert = [(row['grade'], row['name'], row['is_selected']) for index, row in df.iterrows()]

    print(data_to_insert)
    # 插入数据到数据库
    try:
        cursor.executemany("""
        INSERT INTO students (grade, name, is_selected) VALUES (%s, %s, %s)
        """, data_to_insert)
        con.commit()
    except Exception as e:
        con.rollback()
        print(f"An error occurred: {e}")


# 假设Excel文件名为class_list.xlsx
file_path = r'C:\Users\30742\Desktop\class_list.xlsx'
import_from_excel(file_path)

# 关闭连接
con.close()
