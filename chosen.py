import tkinter as tk
from tkinter.font import Font
import time
import pymysql

# 数据库连接参数

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '3074272950',
    'db': 'student',
}

# 连接到数据库
connection = pymysql.connect(**db_config)

# 创建游标
cursor1 = connection.cursor()


# 假设我们已经有了一个名为is_selected的字段，如果没有，请先创建
# ALTER TABLE student_info ADD COLUMN is_selected tinyint(1) DEFAULT 0;


# 定义一个函数用于随机获取两个数据
def fetch_random_data():
    # 初始计数器
    count = 0
    # 初始化text文本框中的内容
    text.delete(1.0, tk.END)

    # 只执行两次获取人名的操作
    while count < 2:
        # 从数据库student的表student_info中获取数据
        sql3 = """
            SELECT grade, name 
            FROM students 
            WHERE is_selected = 0 
            ORDER BY RAND() 
            LIMIT 1
        """
        cursor1.execute(sql3)
        results = cursor1.fetchone()  # 只获取一条记录

        # 获取随机人名
        if results:
            count += 1
            current_time = time.strftime('%Y年%m月%d日 %H:%M:%S', time.localtime())
            count_str = f"\n第{count}次随机抽签({current_time})\n"
            # 将获取的内容添加到text文本框中
            grade, name = results
            text.insert(tk.END, count_str)
            text.insert(tk.END, f"随机演讲的幸运儿是：")
            text.insert(tk.END, f"{grade} {name}\n", "red_id_name")

            # 引入一个时间延迟，保证前后两次时间点不一样
            time.sleep(1)

            # 使用参数化查询插入数据
            sql4 = "INSERT INTO student_info1 (grade, name) VALUES (%s, %s)"
            cursor1.execute(sql4, (grade, name))
            # 更新原表中的is_selected字段
            update_sql = "UPDATE students SET is_selected = 1 WHERE name = %s"
            cursor1.execute(update_sql, (name,))

        else:
            print("没有获取到人名")
            break
    # 提交更改
    connection.commit()


# 定义一个刷新列表以及数据库的函数
def delete_listbox_table():
    try:
        # 执行删除操作
        delete_sql = "DELETE FROM student_info1"
        cursor1.execute(delete_sql)
        connection.commit()
        print("所有数据已成功删除。")
    except Exception as e:
        print(f"删除数据时发生错误：{e}")
        connection.rollback()


# 创建一个主窗口
draw = tk.Tk()  # 生成一个主窗口对象
draw.geometry('600x600')  # 设置窗口的大小
draw.title('抽签')  # 设置窗口的标题

# 创建一个容器来容纳两个listbox
listbox_frame = tk.Frame(draw)
listbox_frame.pack(padx=20, pady=20)

# 创建一个容器来容纳两个button
button_frame = tk.Frame(draw)
button_frame.pack(padx=20, pady=20)

# 创建开始抽签按钮
button1 = tk.Button(button_frame, text="开始抽签", height=2, width=10, bg='white', command=fetch_random_data)
button1.pack(side=tk.LEFT, padx=10, pady=10)


# 填充第二个Listbox的内容
def update_table():
    listbox2.delete(0, tk.END)
    sql2 = "SELECT grade, name FROM student_info1"
    cursor1.execute(sql2)
    for row in cursor1:
        combind_data1 = f"{row[0]}. {row[1]}"
        listbox2.insert(tk.END, combind_data1)


# 创建刷新列表按钮
button2 = tk.Button(button_frame, text="刷新列表", height=2, width=10, bg='white', command=update_table)
button2.pack(side=tk.LEFT, padx=10, pady=10)

# 创建删除数据按钮
button3 = tk.Button(button_frame, text="删除数据", height=2, width=10, bg='white', command=delete_listbox_table)
button3.pack(side=tk.RIGHT, padx=10, pady=10)

# 创建第一个滚动条和列表，将滚动条与Listbox相关联
scrollbar1 = tk.Scrollbar(listbox_frame, takefocus=False, troughcolor="lightgray")
scrollbar1.pack(side=tk.LEFT, fill=tk.Y)
listbox1 = tk.Listbox(listbox_frame, borderwidth=4, width=15)
listbox1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
listbox1.config(yscrollcommand=scrollbar1.set)
scrollbar1.config(command=listbox1.yview)

# 填充第一个Listbox的内容
sql1 = "SELECT grade, name FROM students"
cursor1.execute(sql1)
for row in cursor1:
    combind_data = f"{row[0]}. {row[1]}"
    listbox1.insert(tk.END, combind_data)

# 创建第二个滚动条和列表，将滚动条与Listbox相关联
scrollbar2 = tk.Scrollbar(listbox_frame, takefocus=False, troughcolor="lightgray")
scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
listbox2 = tk.Listbox(listbox_frame, borderwidth=4, width=15)
listbox2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
listbox2.config(yscrollcommand=scrollbar2.set)
scrollbar2.config(command=listbox2.yview)

# 创建一个文本框
text = tk.Text(draw, bd=5)
text.pack(pady=25)

# 设置字体样式
ft = Font(family='宋体', size=14)
listbox1.config(font=ft)
listbox2.config(font=ft)
text.config(font=ft)
button1.config(font=ft)
button2.config(font=ft)
button3.config(font=ft)

# 定义标签和颜色
text.tag_config("red_id_name", foreground="red")

draw.mainloop()
