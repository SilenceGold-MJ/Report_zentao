#!/user/bin/env python3
# -*- coding: utf-8 -*-
from framework.Query_db import Query_DB
from framework.WriteExcle import SummaryExcle
def stets():
    datalist=[{"module":'模块',"sums":'Bug总数', 'closed': '已修复数', 'active': '未修复数', 'resolved': '待验证数'}]
    for n in range(65, 70):

        dic = {"module": n}
        sql = "select count(*) from  zt_bug WHERE project=17 and deleted='0' And module=%s ;" % (n)
        dic.update({'sums': Query_DB().getnum(sql)})
        status_list = ['closed', 'active', 'resolved']
        for i in status_list:
            sql = "select count(*) from  zt_bug WHERE project=17 and deleted='0' And module=%s AND status='%s';" % (
            n, i)
            data = Query_DB().getnum(sql)

            dic.update({i: data})
        datalist.append(dic)
        print(dic)
    return (datalist)

addr='sdsd.xlsx'
SummaryExcle(addr, stets())
