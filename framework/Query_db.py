#!/user/bin/env python3
# -*- coding: utf-8 -*-
import pymysql,re

from framework.logger import Logger
logger = Logger(logger="Query_DB").getlog()

from config.config import *


host=database()['host']
user=database()['user']
password=database()['password']
DB=database()['DB']
port=database()['port']
class Query_DB():#查询个数
    def getnum(self,sql):
        # 打开数据库连接
        db = pymysql.connect(host, user, password, DB)
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # SQL 查询语句
        try:
            # 执行SQL语句
            #logger.info(sql)
            cursor.execute(sql)
            # 获取所有记录列表
            results = str(cursor.fetchall())

            # logger.info(re.findall(r'\d+', results)[0])
            return (int(re.findall(r'\d+', results)[0]))

        except:
            logger.info("Error: unable to fetch data")

        # 关闭数据库连接
        db.close()

    def query_db_all(self,sql ):  # 查询表中所有数据
        lists = []

        # 打开数据库连接

        db = pymysql.connect(host, user, password, DB)
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        #cursor = db.cursor(MySQLdb.cursors.DictCursor)

        try:
            # 执行SQL语句
            # sql = "SELECT * FROM %s"%table_name

            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            desc = cursor.description#提取数据库表头字段
            key_list=( ",".join([item[0] for item in desc]))#提取数据库表头字段
            Key_list =key_list.split(',')#数据库表头字段转化为列表
            for row in results:
                dic = dict(zip(Key_list, row))
                lists.append((dic))
        except Exception as e:
            logger.error(str(e))
        # 关闭数据库连接
        db.close()

        return lists

    def query_db_rowlist(self,sql,row):  # 查询表中某一个行数据列表+除重
        # 打开数据库连接
        db = pymysql.connect(host, user, password, DB)
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        #cursor = db.cursor(MySQLdb.cursors.DictCursor)

        try:
            # 执行SQL语句
            # sql = "SELECT * FROM %s"%table_name
            #sql = "select * from  %s WHERE test_version='%s' AND test_batch='%s' ;" % ( table_name, test_version, test_batch)

            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            key_list=(set ([item[row] for item in results]))
            return list(key_list)

        except Exception as e:
            logger.error(str(e))

        # 关闭数据库连接
        db.close()
    def get_user(self,name ):  # 查询用户信息
        if name=='':
            return '未指派'
        else:
            sql = 'select * from  zt_user WHERE deleted=1 and  account="%s" ;' % (name)

            data_list = Query_DB().query_db_all(sql)[0]
            return data_list['realname']
    def get_bug_list(self,sql):#获取BUG列表
        zentao_host =zentao_Addr()['host']
        zentao_port =zentao_Addr()['port']

        #sql='select * from  zt_bug WHERE module=%s AND deleted=1 AND status!="closed" ORDER BY severity ASC;'%(module)
        data_list=Query_DB().query_db_all(sql)
        datas=[]
        config=configs()
        n=1
        for data in data_list:

            dic = {
                "xulie":n,
                "product": Query_DB().get_product_info(data['product']),
                "module": Query_DB().get_module_info(data['module']),
                'id': data['id'],
                'title': data['title'],
                'severity': config['severity'][str(data['severity'])],
                'pri': config['pri'][str(data['pri'])],
                'status': config['status'][data['status']],
                'openedDate': data['openedDate'],
                'assignedTo': Query_DB().get_user(data['assignedTo']),
                'openedBy': Query_DB().get_user(data['openedBy']),

            }
            n+=1
            datas.append(dic)


        datas_dic={
            'zentao_url': "%s:%s" % (zentao_host, zentao_port),
            'data': datas,
                   }
        return datas_dic
        # import json
        # import datetime
        #
        #
        #
        # class DateEncoder(json.JSONEncoder):
        #     def default(self, obj):
        #         if isinstance(obj, datetime.datetime):
        #             return obj.strftime('%Y-%m-%d %H:%M:%S')
        #         elif isinstance(obj, data):
        #             return obj.strftime("%Y-%m-%d")
        #         else:
        #             return json.JSONEncoder.default(self, obj)
        #
        #
        # datas_str=json.dumps(datas_dic, cls=DateEncoder)
        # return (datas_str)

    def get_product_info(self,product):  # 查询product信息
        sql = 'select * from  zt_product WHERE deleted=1 and  id=%s ;' % (product)
        data_list = Query_DB().query_db_all(sql)[0]
        return data_list['name']

    def get_module_info(self,module):  # 查询用户信息
        sql = 'select * from  zt_module WHERE deleted=1 and  id=%s ;' % (module)
        data_list = Query_DB().query_db_all(sql)[0]
        return data_list['name']
