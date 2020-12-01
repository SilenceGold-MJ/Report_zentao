#!/user/bin/env python3
# -*- coding: utf-8 -*-
import datetime,json
import operator
from framework.Inquiry_info import  *
from config.config import *
from framework.Query_db import Query_DB
from framework.logger import Logger

import configparser,os
proDir = os.getcwd()
configPath = os.path.join(proDir, "config\config.ini")
cf = configparser.ConfigParser()
cf.read(configPath,encoding="utf-8-sig")




logger = Logger(logger="ServiceAPI").getlog()



# print((StartTime + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"))
# # 2019-03-29 17:25:19
# print((StartTime + datetime.timedelta(days=-2)).strftime("%Y-%m-%d %H:%M:%S"))
# # 2019-03-27 17:26:23
class ServiceAPI():
    def grow_days_zs(self,dic):#天增长

        def timeweek(time_rq):
            from datetime import datetime
            week = datetime.strptime(time_rq, "%Y-%m-%d").weekday()
            return week
        StartTime_srt = '%s 00:00:00'%(dic['StartTime'])
        End_Time_srt= '%s 23:59:59'%(dic['End_Time'])
        StartTime = datetime.datetime.strptime(StartTime_srt, '%Y-%m-%d %H:%M:%S')
        # End_Times = datetime.datetime.strptime(End_Time_srt, '%Y-%m-%d %H:%M:%S')
        # #now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        Wkhours = ((datetime.datetime.strptime(End_Time_srt, '%Y-%m-%d %H:%M:%S') - StartTime).days)
        totallist=[]
        submodule=[]
        days_list=[]
        week_list=[]
        number_zs_list=[]
        products=[]
        modules=[]

        for i in range(0, Wkhours + 1):
            End_Time = ((StartTime + datetime.timedelta(days=i)).strftime("%Y-%m-%d 23:59:59"))
            if dic['module']=="" and dic['product']!='':
                product = get_product_info(dic['product'])
                module =''
                sql_xm = "SELECT count(*) FROM zt_bug WHERE product=%s and deleted='0' and	openedDate  between '%s' and '%s';" % (dic['product'],StartTime_srt, End_Time)
            elif dic['module'] != "" and dic['product'] == '':
                product = ''
                module = get_module_info(dic['module'])

                sql_xm = "SELECT count(*) FROM zt_bug WHERE module=%s and deleted='0' and	openedDate  between '%s' and '%s';" % (dic['module'], StartTime_srt, End_Time)
            else:
                product = get_product_info(dic['product'])
                module = get_module_info(dic['module'])
                sql_xm="SELECT count(*) FROM zt_bug WHERE product=%s and deleted='0' and module=%s and openedDate  between '%s' and '%s';" % (dic['product'],dic['module'],StartTime_srt, End_Time)

            days_time = datetime.datetime.strptime(StartTime_srt, '%Y-%m-%d %H:%M:%S').strftime("%Y-%m-%d")

            total={
                'days': days_time,
                'week':timeweek(days_time)+1,
                 'number_zs': Query_DB().getnum(sql_xm),

            }
            # sub={
            #     'days': days_time,
            #     'week': timeweek(days_time) + 1,
            #
            #     'number_mk': Query_DB().getnum(sql_zmk),
            # }
            totallist.append( total)
            days_list.append(total['days'])
            week_list.append(total['week'])
            number_zs_list.append(total['number_zs'])
            products.append(product)
            modules.append(module)
            #submodule.append(sub)

            StartTime_srt = ((StartTime + datetime.timedelta(days=i + 1)).strftime("%Y-%m-%d %H:%M:%S"))

        data = {
            'total': totallist,
            'sub': submodule
        }
        return {
                'message': '操作成功',
                'result_code': '0000',
                'product': products[0],
                'module': modules[0],
                'data':totallist,
                'days_list':days_list,
                "week_list":week_list,
                "number_zs_list":number_zs_list
                }

    def get_module(self,product):  # 获取项目下的模块
        sql="select * from  zt_module WHERE root=%s and (type='bug' or type='story')  and deleted='0' ;"%(product)
        data=Query_DB().query_db_rowlist(sql,0)#
        alldata=Query_DB().query_db_all(sql)

        diclist={}
        for i in data:
            for n in alldata:

                if i == n['id']:
                    diclist.update({str(i): n['name']})


        return {'message': '操作成功', 'result_code': '0000', 'data':{"modulelist":data,'Modulename':diclist} }

    def module_info(self,product):#各个模块详情

        projects_info = ((ServiceAPI().get_module(product)))
        datalists=[]
        Modulename_list=[]
        msdule_num=[]

        for n in projects_info['data']['modulelist']:

            dic = {"module": n,'Modulename':projects_info['data']['Modulename'][str(n)],}
            sql = "select count(*) from  zt_bug WHERE product=%s and deleted='0' And module=%s ;" % (product,n)
            dic.update({'sums': Query_DB().getnum(sql)})
            status_list = ['closed', 'active', 'resolved']
            for i in status_list:
                sql = "select count(*) from  zt_bug WHERE product=%s and deleted='0' And module=%s AND status='%s';" % (product,
                    n, i)
                data = Query_DB().getnum(sql)

                dic.update({i: data})
            for i in severity():
                sql = "select count(*) from  zt_bug WHERE product=%s and deleted='0' and status!='closed' And module=%s AND severity=%s;" % (product,
                    n, i)
                data = Query_DB().getnum(sql)

                dic.update({"severity_%s"%i: data})

            dic.update({'Repair_rate': round(dic['closed'] / dic['sums'], 4) if dic['sums']!=0 else 0.0})
            dic.update({"owner":get_module_info(n)["owner"]})#责任人
            dic.update(status_Rele(dic))

            Modulename_list.append(dic['Modulename'])
            msdule_num.append(dic['sums'])
            datalists.append(dic)

        Repair_rate = sorted(datalists, key=lambda i: i['Repair_rate'], reverse=False)  # 降序

        product_name_r = []
        Repair_rate_r = []
        for i in Repair_rate:
            product_name_r.append(i['Modulename'])
            Repair_rate_r.append(i['Repair_rate'])

        Repair_rate_dic_sorted = {'product_name_r': product_name_r, 'Repair_rate_r': Repair_rate_r}

        dic = {'message': '操作成功',
               'result_code': '0000',
               'data': datalists,
               'Modulename_list':Modulename_list,
               'msdule_num':msdule_num,
               'Repair_rate_dic_sorted':Repair_rate_dic_sorted,
               'Repair_datalists_sorted':Repair_rate

               }
        dic_srt = json.dumps(dic)
        return dic_srt
    def get_product(self):#获取项目信息
        sql ='select * from  zt_product WHERE deleted="0";'
        data = Query_DB().query_db_all(sql)
        dic={'message': '操作成功', 'result_code': '0000', 'data':data }
        #dic_srt=json.dumps(dic)
        return dic

    def get_All_projects(self):#获取所有项目信息
        sql ='select * from  zt_product WHERE deleted="0" ORDER BY id DESC;'
        All_projects = Query_DB().query_db_all(sql)
        #All_projects=sorted(All_projects, key=operator.itemgetter('id'), reverse=True)#排序降序
        data=[]
        product_name=[]
        product_sum=[]
        Repair_rate={}
        n=1
        for i in All_projects:
            sql_sum_all="select count(*) from  zt_bug WHERE product=%s and deleted='0';" % (i["id"])
            status_list = ['closed', 'active', 'resolved']

            data_dic={
                #"ID":n,
                'product':i["id"],
                'name':i["name"],
                'sum_all': Query_DB().getnum(sql_sum_all),
                #'module_info':ServiceAPI().module_info(i["id"]),

            }
            for status in status_list :
                sql_sum = "select count(*) from  zt_bug WHERE product=%s and deleted='0'  AND status='%s';" % (i["id"], status)

                data_dic.update({status:Query_DB().getnum(sql_sum)})

            for s in severity() :
                sql_sum = "select count(*) from  zt_bug WHERE product=%s and deleted='0'  AND severity='%s' and status!='closed';" % (i["id"], s)

                data_dic.update({"severity_%s"%s:Query_DB().getnum(sql_sum)})


            data_dic.update({'Repair_rate': round(data_dic['closed'] / data_dic['sum_all']  if data_dic['sum_all']!=0 else 0.0,4),"PO":get_product_info_(i["id"])["PO"]})


            n+=1
            data.append(data_dic)
            data_dic.update(status_Rele(data_dic))

            product_name.append(data_dic['name'])
            product_sum.append(data_dic['sum_all'])
            Repair_rate.update({i["name"]:round(data_dic['closed'] / data_dic['sum_all'] if data_dic['sum_all']!=0 else 0.0,4)})

        Repair_rate=sorted(data, key = lambda i: i['Repair_rate'],reverse=False)#降序

        product_name_r=[]
        Repair_rate_r=[]
        for i in Repair_rate:
            product_name_r.append(i['name'])
            Repair_rate_r.append(i['Repair_rate'])


        Repair_rate_dic_sorted = {'product_name_r':product_name_r,'Repair_rate_r':Repair_rate_r}

        dic={'message': '操作成功', 'result_code': '0000', 'data':data,'product_name':product_name,'product_sum':product_sum ,'Repair_rate_sorted':Repair_rate,'Repair_rate_dic_sorted':Repair_rate_dic_sorted }
        dic_srt=json.dumps(dic)
        return dic_srt
    def get_module_bug(self,module):#获取模块未关闭BUG列表

        zentao_host =zentao_Addr()['host']
        zentao_port =zentao_Addr()['port']

        #sql='select * from  zt_bug WHERE module=%s AND deleted="0" AND status!="closed" ORDER BY severity ASC;'%(module)
        sql='select * from  zt_bug WHERE module=%s and deleted="0" and status!="closed" order  by severity asc,pri asc;'%(module)

        data_list=Query_DB().query_db_all(sql)
        datas=[]
        config=configs()
        n=1
        for data in data_list:

            dic = {
                "xulie":n,
                "product":get_product_info(data['product']),
                "module":get_module_info(data['module'])['module'],
                'id': data['id'],
                'title': data['title'],
                'severity': config['severity'][str(data['severity'])],
                'pri': config['pri'][str(data['pri'])],
                'status': config['status'][data['status']],
                'openedDate': data['openedDate'],
                'assignedTo': ServiceAPI(). get_user(data['assignedTo']),
                'openedBy': ServiceAPI(). get_user(data['openedBy']),

            }
            n+=1
            datas.append(dic)
        datas_dic={'message': '操作成功', 'result_code': '0000', 'data': datas,'zentao_url':"%s:%s"%(zentao_host,zentao_port)}
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


        datas_str=json.dumps(datas_dic, cls=DateEncoder)
        return (datas_str)

    def get_user(self,name ):  # 查询用户信息
        if name=='':
            return '未指派'
        else:
            sql = 'select * from  zt_user WHERE deleted="0" and  account="%s" ;' % (name)

            data_list = Query_DB().query_db_all(sql)[0]
            return data_list['realname']

    def get_product_sum(self,dic):#
        dic_data={}
        if dic['module'] == "" and dic['product'] != '':
            sql_product = "select * from  zt_product WHERE id=%s ;" % (dic['product'])
            sql_all = 'select count(*) from  zt_bug WHERE product=%s and deleted="0";' % (dic['product'])
            for i in status():
                sql_status = 'select count(*) from  zt_bug WHERE product=%s and deleted="0" and status="%s" ;' % (dic['product'], i)

                dic_data.update({i: Query_DB().getnum(sql_status)})


        elif dic['module'] != "" and dic['product'] == '':

            sql_product = "select * from  zt_module WHERE id=%s ;" % (dic['module'])
            sql_all = 'select count(*) from  zt_bug WHERE module=%s and deleted="0";' % (dic['module'])

            for i in status():
                sql_status = 'select count(*) from  zt_bug WHERE module=%s and deleted="0" and status="%s" ;' % (dic['module'], i)

                dic_data.update({i: Query_DB().getnum(sql_status)})

        else:
            sql_product = "select * from  zt_module WHERE id=%s ;" % (dic['module'])
            sql_all = 'select count(*) from  zt_bug WHERE module=%s and deleted="0";' % (dic['module'])
            for i in status():
                sql_status = 'select count(*) from  zt_bug WHERE module=%s and deleted="0" and status="%s" ;' % (dic['module'], i)

                dic_data.update({i: Query_DB().getnum(sql_status)})



        dic_da= {'message': '操作成功',
                    'result_code': '0000',
                    "data":{
                        'name':Query_DB().query_db_all(sql_product)[0]['name'],
                        'sum_all':Query_DB().getnum(sql_all),
                        'data': dic_data
                    }
                    }
        dic_srt = json.dumps(dic_da)
        return dic_srt

    def get_product_module_sum(self,dic):#获取项目近况数据
        dic_data={}
        if dic['module'] == "" and dic['product'] != '':
            sql_product = "select * from  zt_product WHERE id=%s ;" % (dic['product'])
            sql_all = 'select count(*) from  zt_bug WHERE product=%s and deleted="0";' % (dic['product'])
            dic_data.update(
                {'product': Query_DB().query_db_all(sql_product)[0]['name'], 'module': '',
                 'bug_total': Query_DB().getnum(sql_all), })
            for i in status():
                sql_status = 'select count(*) from  zt_bug WHERE product=%s and deleted="0" and status="%s" ;' % (dic['product'], i)

                dic_data.update({"%s_sum" % i: Query_DB().getnum(sql_status)})

            for i in severity():
                sql_status = 'select count(*) from  zt_bug WHERE product=%s and deleted="0" and severity=%s and status!="closed";' % (dic['product'], i)

                dic_data.update({'severity_%s'%i: Query_DB().getnum(sql_status)})

        elif dic['module'] != "" and dic['product'] == '':

            sql_all = 'select count(*) from  zt_bug WHERE module=%s and deleted="0";' % (dic['module'])
            dic_data.update(get_module_info( dic['module']))
            dic_data.update({'bug_total': Query_DB().getnum(sql_all), })
            for i in status():
                sql_status = 'select count(*) from  zt_bug WHERE module=%s and deleted="0" and status="%s" ;' % (dic['module'], i)

                dic_data.update({"%s_sum" % i: Query_DB().getnum(sql_status)})
            for i in severity():
                sql_status = 'select count(*) from  zt_bug WHERE module=%s and deleted="0" and severity=%s and status!="closed";' % (dic['module'], i)

                dic_data.update({'severity_%s'%i: Query_DB().getnum(sql_status)})

        else:

            sql_all = 'select count(*) from  zt_bug WHERE module=%s and deleted="0";' % (dic['module'])
            dic_data.update(get_module_info( dic['module']))
            dic_data.update({'bug_total': Query_DB().getnum(sql_all), })
            for i in status():
                sql_status = 'select count(*) from  zt_bug WHERE module=%s and deleted="0" and status="%s" ;' % (dic['module'], i)

                dic_data.update({"%s_sum" % i: Query_DB().getnum(sql_status)})
            for i in severity():
                sql_status = 'select count(*) from  zt_bug WHERE module=%s and deleted="0" and severity=%s and status!="closed";' % (dic['module'], i)

                dic_data.update({'severity_%s'%i: Query_DB().getnum(sql_status)})

        # dic_new={
        # 	'product':'',
        # 	'module': '',
        # 	'bug_total':"",
        # 	'closed_sum': "关闭",
        # 	'active_sum': "激活",
        # 	'resolved_sum': "待验证",
        # 	'severity_1': '',
        # 	'severity_2': '',
        # 	'severity_3': '',
        # 	'severity_4': '',
        # }


        dic_da= {'message': '操作成功',
                    'result_code': '0000',
                    "data":dic_data

                    }
        dic_srt = json.dumps(dic_da)
        return dic_srt


    def Check_new_BUG(self,dic):
        if dic['module'] == "" and dic['product'] != '':
            sql_DESC = 'select * from  zt_bug WHERE product=%s and deleted="0" ORDER BY openedDate DESC LIMIT 0,1;' % (dic['product'])

            sql_ASC = 'select * from  zt_bug WHERE product=%s and deleted="0" ORDER BY openedDate ASC LIMIT 0,1;' % (dic['product'])
            product =dic['product']

        elif  dic['module'] != "" and dic['product'] == '':
            product = get_module_info(dic['module'])['product_id']
            sql_DESC = 'select * from  zt_bug WHERE module=%s and deleted="0" ORDER BY openedDate DESC LIMIT 0,1;' % (dic['module'])

            sql_ASC = 'select * from  zt_bug WHERE module=%s and deleted="0" ORDER BY openedDate ASC LIMIT 0,1;' % (dic['module'])

        else:
            product = get_module_info(dic['module'])['product_id']
            sql_DESC = 'select * from  zt_bug WHERE module=%s and deleted="0" ORDER BY openedDate DESC LIMIT 0,1;' % (dic['module'])

            sql_ASC = 'select * from  zt_bug WHERE module=%s and deleted="0" ORDER BY openedDate ASC LIMIT 0,1;' % (dic['module'])
        data_list=Query_DB().query_db_all(sql_DESC)
        if len(data_list)!=0:
            data_list = data_list[0]['openedDate']
            start_time = Query_DB().query_db_all(sql_ASC)[0]['openedDate']
        else:
            import time
            dt = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

            sql_start='SELECT * FROM zt_product WHERE id= %s;'%(product)
            data_list =dt
            start_time =Query_DB().query_db_all(sql_start)[0]['createdDate']


        dic_data = {'message': '操作成功',
                    'result_code': '0000',
                    "End_Time":str(data_list).split(" ")[0],#data_list#
                    'StartTime':str(start_time).split(" ")[0]#data_list#
                    }
        import json
        import datetime

        class DateEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, datetime.datetime):
                    return obj.strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(obj, data_list):
                    return obj.strftime("%Y-%m-%d")
                else:
                    return json.JSONEncoder.default(self, obj)
        dic_srt = json.dumps(dic_data , cls=DateEncoder)
        return dic_srt
    def Importance_level(self,dic):#获取严重级别以上BUG

        sql_pro='select * from  zt_bug WHERE deleted="0" and product=%s AND status!="closed" AND severity%s ORDER BY pri ASC;'%(dic['product'],dic['severity'])
        sql_pro_module = 'select * from  zt_bug WHERE deleted="0" and product=%s AND module=%s AND status!="closed" AND severity%s ORDER BY pri ASC;'%(dic['product'],dic['module'],dic['severity'])
        sql_module = 'select * from  zt_bug WHERE deleted="0" and module=%s AND status!="closed" AND severity%s ORDER BY pri ASC;' % (dic['module'],dic['severity'])

        if dic['module']=="" and dic['product']!='':
            product=get_product_info(dic['product'])
            module=''
            data_dic = Query_DB().get_bug_list(sql_pro)
        elif dic['module']!="" and dic['product']=='':
            module=get_module_info(dic['module'])
            product=''
            data_dic = Query_DB().get_bug_list(sql_module)
        else:
            product = get_product_info(dic['product'])
            module = get_module_info(dic['module'])
            data_dic = Query_DB().get_bug_list(sql_pro_module)

        import json
        import datetime

        class DateEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, datetime.datetime):
                    return obj.strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(obj, data_dic):
                    return obj.strftime("%Y-%m-%d")
                else:
                    return json.JSONEncoder.default(self, obj)


        dic_data = {'message': '操作成功',
                    'result_code': '0000',
                    'data':data_dic


                    }
        (dic_data['data'].update({"product": product, "module": module}))
        dic_srt = json.dumps(dic_data , cls=DateEncoder)
        return dic_srt

    def get_severity(self,dic):#获取严重程度数量扇形图基础数据

        severity_name_all = []
        severity_sums_all= []
        severity_name_NOclosed=[]
        severity_sums_NOclosed=[]
        products=[]
        modules=[]
        for key_severity,values_severity in configs()['severity'].items():

            sql_product_all='select count(*) from  zt_bug WHERE deleted="0" and  severity=%s and product=%s ;'%(key_severity,dic['product'])
            sql_module_all='select count(*) from  zt_bug WHERE deleted="0" and  severity=%s  AND module=%s;'%(key_severity,dic['module'])
            sql_module_product_all = 'select count(*) from  zt_bug WHERE deleted="0" and  severity=%s and product=%s AND module=%s;'%(key_severity,dic['product'],dic['module'])

            sql_product_NOclosed = 'select count(*) from  zt_bug WHERE deleted="0" and  severity=%s and product=%s and status!="closed" ;' % (
            key_severity, dic['product'])
            sql_module_NOclosed = 'select count(*) from  zt_bug WHERE deleted="0" and  severity=%s  AND module=%s and status!="closed";' % (
            key_severity, dic['module'])
            sql_module_product_NOclosed = 'select count(*) from  zt_bug WHERE deleted="0"and  severity=%s and product=%s AND module=%s and status!="closed";' % (
            key_severity, dic['product'], dic['module'])

            if dic['module'] == "" and dic['product'] != '':
                product = get_product_info(dic['product'])
                module =  ''
                severity_sum_all=Query_DB().getnum(sql_product_all)
                severity_sum_NOclosed = Query_DB().getnum(sql_product_NOclosed)
            elif dic['module'] != "" and dic['product'] == '':
                product =  ''
                module = get_module_info(dic['module'])
                severity_sum_all = Query_DB().getnum(sql_module_all)
                severity_sum_NOclosed = Query_DB().getnum(sql_module_NOclosed)
            elif dic['module'] != "" and dic['product'] != '':
                product = get_product_info(dic['product'])
                module = get_module_info(dic['module'])
                severity_sum_all = Query_DB().getnum(sql_module_product_all)
                severity_sum_NOclosed = Query_DB().getnum(sql_module_product_NOclosed)
            else:
                product = ''
                module =  ''
                severity_sum_all=-1
                severity_sum_NOclosed = -1
            severity_sums_all.append(severity_sum_all)
            severity_name_all.append(values_severity)
            severity_sums_NOclosed.append(severity_sum_NOclosed)
            severity_name_NOclosed.append(values_severity)
            products.append(product)
            modules.append(module)


        dic={
            'product':products[0],
            'module':modules[0],
            "severity_all":{
                "severity_name_all":severity_name_all,
                "severity_sums_all":severity_sums_all
            },
            'severity_NOclosed':{
                'severity_name_NOclosed':severity_name_NOclosed,
                'severity_sums_NOclosed':severity_sums_NOclosed

            }

        }

        dic_data = {'message': '操作成功',
                    'result_code': '0000',
                    "data":dic
                    }
        dic_srt = json.dumps(dic_data)
        return dic_srt
