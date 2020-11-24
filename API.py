#!/user/bin/env python3
# -*- coding: utf-8 -*-
import flask, json,os
import datetime
from flask import request

from framework.ServiceAPI import ServiceAPI
from framework.logger import Logger
logger = Logger(logger="API").getlog()

'''
flask： web框架，通过flask提供的装饰器@server.route()将普通函数转换为服务
'''
# 创建一个服务，把当前这个python文件当做一个服务
server = flask.Flask(__name__)

# server.config['JSON_AS_ASCII'] = False
# @server.route()可以将普通函数转变为服务 的路径、请求方式
@server.route('/grow_days', methods=['post'])#'get',
def grow_days():#日增
    params = flask.request.json  # 当客户端没有传json类型或者没传时候，直接get就会报错。
    if params:
        dic = {
            'product':params.get('product'),
            'module': params.get('module'),
            'StartTime': params.get('StartTime'),
            'End_Time': params.get('End_Time'),  # datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        data = json.dumps(ServiceAPI().grow_days_zs(dic))
        logger.info("'/grow_days',methods=['post']" +str(data))
        return data
    else:
        data = json.dumps({"result_code": 3002, "msg": "入参必须为json类型。"})
        logger.info("'/grow_days',methods=['post']" + str(data))
        return data

@server.route('/get_module', methods=['post'])#'get',
def get_module():#获取项目下的模块
    params = flask.request.json  # 当客户端没有传json类型或者没传时候，直接get就会报错。
    if params:

        product=params.get('product')


        data = json.dumps(ServiceAPI().get_module(product))
        logger.info("'/get_module',methods=['post']" +str(data))
        return data
    else:
        data = json.dumps({"result_code": 3002, "msg": "入参必须为json类型。"})
        logger.info("'/get_module',methods=['post']："+str(data))
        return data
@server.route('/get_product', methods=['post'])#'get',
def get_product():#获取项目信息
    import json
    import datetime

    class DateEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime.datetime):
                return obj.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(obj, data):
                return obj.strftime("%Y-%m-%d")
            else:
                return json.JSONEncoder.default(self, obj)

                #data = json.dumps(ServiceAPI().get_product())
    data = (ServiceAPI().get_product())
    logger.info("'/get_product',methods=['post']" + str(data))
    return json.dumps(data, cls=DateEncoder)
@server.route('/get_All_projects', methods=['post'])#'get',
def get_All_projects():#获所有项目信息

    data = (ServiceAPI().get_All_projects())
    logger.info("'/get_All_projects',methods=['post']" + str(data))
    return data
@server.route('/module_info', methods=['post'])#'get',
def module_info():#获模块信息
    params = flask.request.json  # 当客户端没有传json类型或者没传时候，直接get就会报错。
    if params:

        product=params.get('product')

        data = (ServiceAPI().module_info(product))
        logger.info("'/get_All_projects',methods=['post']" + str(data))
        return data
    else:
        data = json.dumps({"result_code": 3002, "msg": "入参必须为json类型。"})
        logger.info("'/get_All_projects',methods=['post']："+str(data))
        return data
@server.route('/get_module_bug', methods=['post'])#'get',
def get_module_bug():#获取模块未关闭的BUG
    params = flask.request.json  # 当客户端没有传json类型或者没传时候，直接get就会报错。
    if params:

        module = params.get('module')

        data = (ServiceAPI().get_module_bug(module))
        logger.info("'/get_All_projects',methods=['post']" + str(data))
        return data
    else:
        data = json.dumps({"result_code": 3002, "msg": "入参必须为json类型。"})
        logger.info("'/get_All_projects',methods=['post']：" + str(data))
        return data

@server.route('/get_product_sum', methods=['post'])#'get',
def get_product_sum():#获取某个项目数量
    params = flask.request.json  # 当客户端没有传json类型或者没传时候，直接get就会报错。
    if params:
        dic={"product": params.get('product'),"module":params.get('module')}

        data = (ServiceAPI().get_product_sum(dic))
        logger.info("'/get_product_sum',methods=['post']" + str(data))
        return data
    else:
        data = json.dumps({"result_code": 3002, "msg": "入参必须为json类型。"})
        logger.info("'/get_product_sum',methods=['post']：" + str(data))
        return data
@server.route('/Check_new_BUG', methods=['post'])#'get',
def Check_new_BUG():
    params = flask.request.json  # 当客户端没有传json类型或者没传时候，直接get就会报错。
    if params:
        dic={"product": params.get('product'),"module":params.get('module')}
        data = (ServiceAPI().Check_new_BUG(dic))
        logger.info("'/get_product_sum',methods=['post']" + str(data))
        return data
    else:
        data = json.dumps({"result_code": 3002, "msg": "入参必须为json类型。"})
        logger.info("'/get_product_sum',methods=['post']：" + str(data))
        return data
@server.route('/Importance_level', methods=['post'])#'get',
def Importance_level():#获取未关闭严重级别以上BUG
    params = flask.request.json  # 当客户端没有传json类型或者没传时候，直接get就会报错。
    if params:

        dic = {
            "product": params.get('product'),
            "module": params.get('module'),
            'severity':params.get('severity'),#'severity<=2'
        }
        data = (ServiceAPI().Importance_level(dic))
        logger.info("'/get_product_sum',methods=['post']" + str(data))
        return data
    else:
        data = json.dumps({"result_code": 3002, "msg": "入参必须为json类型。"})
        logger.info("'/get_product_sum',methods=['post']：" + str(data))
        return data
@server.route('/get_severity', methods=['post'])#'get',
def get_severity():#获取严重程度扇形图的基础数据
    params = flask.request.json  # 当客户端没有传json类型或者没传时候，直接get就会报错。
    if params:

        dic = {
            "product": params.get('product'),
            "module": params.get('module')
        }
        data = (ServiceAPI().get_severity(dic))
        logger.info("'/get_severity',methods=['post']" + str(data))
        return data
    else:
        data = json.dumps({"result_code": 3002, "msg": "入参必须为json类型。"})
        logger.info("'/get_severity',methods=['post']：" + str(data))
        return data

@server.route('/get_product_module_sum', methods=['post'])#'get',
def get_product_module_sum():#获取项目近况数据
    params = flask.request.json  # 当客户端没有传json类型或者没传时候，直接get就会报错。
    if params:

        dic = {
            "product": params.get('product'),
            "module": params.get('module')
        }
        data = (ServiceAPI().get_product_module_sum(dic))
        logger.info("'/get_product_module_sum,methods=['post']" + str(data))
        return data
    else:
        data = json.dumps({"result_code": 3002, "msg": "入参必须为json类型。"})
        logger.info("'/get_product_module_sum',methods=['post']：" + str(data))
        return data

if __name__ == '__main__':
    server.run(debug=True, port=9001, host='0.0.0.0')  # 指定端口、host,0.0.0.0代表不管几个网卡，任何ip都可以访问
