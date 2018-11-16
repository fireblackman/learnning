#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-15 13:09:01
# @Author  : zhangsir (1007072466@qq.com)
# @Link    : ${link}
# @Version : $Id$

import pymysql

# 1.创建数据库连接对象
db = pymysql.connect(host="localhost",user="root",password="123456")
# 2.创建游标对象(利用数据库的对象)
cursor = db.cursor()

# 3.执行SQL命令(利用游标对象)
#-----------创建库-------------------
sql = 'create database pymysql_test charset=utf8;'
cursor.execute(sql)
db.commit()
sql = "use pymysql_test;"
cursor.execute(sql)
db.commit()


# #-----------创建表-------------------
sql = "create table t1(id int,name varchar(20),age tinyint unsigned)charset=utf8 engine=innodb;"
cursor.execute(sql)
db.commit()

#-----------表字段增改删查--------------
sql = "desc t1;"
cursor.execute(sql)
db.commit()

sql = "alter table t1 add score float(5,2);"
cursor.execute(sql)
db.commit()

sql = "alter table t1 modify age int;"
cursor.execute(sql)
db.commit()

sql = "alter table t1 drop score;"
cursor.execute(sql)
db.commit()



#-----------表记录增改删查-------------
sql= 'insert into t1 values(1,"wangwei",80),(2,"libai",80),(3,"mengjiao",80),(4,"dufu",80);'
cursor.execute(sql)
db.commit()

sql = "select * from t1;"
cursor.execute(sql)
db.commit()

sql = "delete from t1 where id=1;"
cursor.execute(sql)
db.commit()

sql = "update t1 set name='wangwei',age=18 where id=3;"
cursor.execute(sql)
db.commit()


#-----------查询常用函数---------------
sel = "select * from t1"
try:
    # 得到一堆查询结果，放到了cursor游标对象里
    cursor.execute(sel)
    # # fetchone取走游标对象里的1条记录
    data1 = cursor.fetchone()
    print(data1)
    print("*" * 40)
    
    # 取走游标对象里的多条记录 
    data2 = cursor.fetchmany(2)
    # data2 : ((2,"李白",80),(3,...))
    for r in data2:
        print(r)
    print("*" * 40)

    # 取走游标对象中剩下的表记录
    data3 = cursor.fetchall()
    print(data3)
except Exception as e:
    print("Failed",e)


# 4.提交到数据库执行(commit())
db.commit()
print("ok")

# 5.关闭游标对象
cursor.close()

# 6.关闭数据库连接对象
db.close()
