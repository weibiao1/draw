import pymongo
import random

myclient = pymongo.MongoClient("mongodb://localhost:27017/")


def get_str(a, b):
    return random.randint(a, b)


def get_data_list(m):
    getdata_list = []
    for _ in range(m):
        x = 0
        x += 1
        data_dict = {'name': get_str(2, 4), 'passwd': get_str(8, 12)}
        getdata_list.append(data_dict)
    return getdata_list


if __name__ == '__main__':
    print("建立连接...")
    mydb = myclient["stus"]  # 创建数据库
    stus = mydb["stu"]  # 创建表

    # 插入一条记录
    print("插入一条记录...")
    getdata = {'name': get_str(2, 4), 'passwd': get_str(8, 12)}
    stus.insert_one(getdata)  # 向表中添加数据
    # 显示所有记录
    print("显示所有记录...")
    stus_find = stus.find_one({'name': getdata['name'], 'passwd': getdata['passwd']})
    print(stus_find)

    # 批量插入多条记录
    print("批量插入多条记录...")
    stus.insert_many(get_data_list(3))
    # 显示所以有记录
    print("显示所有记录...")
    for stu in stus.find():
        print(stu)

    # 更新一条记录
    print("更新一条记录...")
    nam = int(input("请输入记录的name:"))  # 提示输入要修改的数据
    nam_1 = str(input("请输入修改的数据:"))
    stus.update_many({'name': nam}, {'$set': {'name': nam_1}})
    # 显示所以有记录
    print("显示所有记录...")
    for stu in stus.find():
        print(stu)

    # s删除一条记录
    print("删除一条记录...")
    nam = int(input("请输入记录的name:"))
    stus.delete_many({'name': nam})  # 删除表中的数据
    print("显示所有记录...")
    for stu in stus.find():
        print(stu)
