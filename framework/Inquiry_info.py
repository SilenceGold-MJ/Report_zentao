#!/user/bin/env python3
# -*- coding: utf-8 -*-
from config.config import *
from framework.Query_db import Query_DB
def get_product_info_( product):  # 查询product信息
    sql = 'select * from  zt_product WHERE deleted=1 and  id=%s ;' % ( product)

    data_list = Query_DB().query_db_all(sql)[0]
    sql_name = 'SELECT * FROM zt_user WHERE account="%s";' % (data_list['PO'])

    return {
        'product_name':data_list['name'],
        'product_id': product,
        "PO":Query_DB().query_db_all(sql_name)[0]['realname'] if data_list['PO']!="" else '未指派'
    }

def get_product_info( product):  # 查询product信息
    sql = 'select * from  zt_product WHERE deleted=1 and  id=%s ;' % ( product)

    data_list = Query_DB().query_db_all(sql)[0]
    return data_list['name']
def get_module_info( module):  # 查询用户信息
    sql = 'select * from  zt_module WHERE deleted=1 and  id=%s ;' % ( module)
    data_list = Query_DB().query_db_all(sql)[0]

    sql_name='SELECT * FROM zt_user WHERE account="%s";' % (data_list['owner'])
    return {
        'product':get_product_info(data_list['root']),
        'module':data_list['name'],
        'product_id': data_list['root'],
        'owner':Query_DB().query_db_all(sql_name)[0]['realname'] if data_list['owner']!="" else '未指派',
    }

def status_Rele(dci):
    repair_threshold=Repair_threshold()#修复率阀值


    if 'sum_all' in dci:
        if dci['sum_all']!=0:
            if dci['Repair_rate']>repair_threshold:
                if dci['severity_1'] + dci['severity_2'] == 0 and dci['severity_3'] == 0 and dci['severity_4'] == 0:
                    return {'status_Rele': '发布正式'}
                elif dci['severity_1'] + dci['severity_2'] == 0 and dci['severity_3'] == 0:
                    return {'status_Rele': '发布正式'}
                elif dci['severity_1'] + dci['severity_2'] == 0:
                    return {'status_Rele': '发布试用'}
                elif dci['severity_1'] + dci['severity_2'] > 0:
                    return {'status_Rele': '不可发布'}
            else:
                return {'status_Rele': '不可发布'}
        else:
            return {'status_Rele': '未开始'}


    elif 'sums' in dci:
        if dci['sums']!=0:
            if dci['Repair_rate'] > repair_threshold:
                if dci['severity_1'] + dci['severity_2'] == 0 and dci['severity_3'] == 0 and dci['severity_4'] == 0:
                    return {'status_Rele': '发布正式'}
                elif dci['severity_1'] + dci['severity_2'] == 0 and dci['severity_3'] == 0:
                    return {'status_Rele': '发布正式'}
                elif dci['severity_1'] + dci['severity_2'] == 0:
                    return {'status_Rele': '发布试用'}
                elif dci['severity_1'] + dci['severity_2'] > 0:
                    return {'status_Rele': '不可发布'}
            else:
                return {'status_Rele': '不可发布'}
        else:
            return {'status_Rele': '未开始'}


