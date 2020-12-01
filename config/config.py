
def database():#数据库地址
	dic={
		"host":"192.168.1.55",#127.0.0.1"
		'user':'root',
		'password' : "hl123456",
		'DB':'zentao',
		'port':3306
	}
	return dic

def zentao_Addr():#禅道地址
	dic={
		"host":"192.168.1.55",
		'port':81

	}
	return dic




def configs():
	config = {
		"severity": {
			"1": "致命",
			"2": "严重",
			"3": "一般",
			"4": "轻微",

		},
		"status": {
			'closed': "关闭",
			'active': "激活",
			'resolved': "待验证"
		},
		'pri': {
			"1": "紧急",
			"2": "高",
			"3": "中",
			"4": "低",
		}
	}

	return config
def status():

	return ['closed','active','resolved']

def severity():
	return ["1","2","3","4"]


def Repair_threshold():#修复率阀值
	repair_threshold=0.8  #修复率阀值
	return repair_threshold
