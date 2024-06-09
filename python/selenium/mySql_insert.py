import pymysql

# 连接数据库
db = pymysql.connect(host="localhost", user="root", passwd="3074272950", database="SYS", port=3306)
# 使用cursor()方法操作游标
cursor = db.cursor()
# SQL插入语句
sql = """insert into test(first_name,last_name,age,sex,income)
          values('Mac','Mohan','22','M',2000)"""
try:
    # 执行SQL语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
except:
    # 如果发生错误则回滚
    db.rollback()
# 关闭数据库连接
db.close()

