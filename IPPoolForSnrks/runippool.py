"""
运行ip池
"""
import time
import traceback
from IPPoolForSnrks.spiders import proxyspider
from IPPoolForSnrks.validate import validate
from IPPoolForSnrks.CheckFromDb import CheckFromDb
from log import Logger

log = Logger().log()
check = CheckFromDb()

def run_add_pool():
	"""
	运行增加IP POOL
	:return:
	"""
	spider = proxyspider()
	spideData = spider.spiderFromXici()
	newIPS = check.if_update(spideData)
	if newIPS['isupdate'] == True:
		available_ip, unavailable_ip = validate().validate(ips=newIPS['data'])
		check.inserte_into_db(list=available_ip)
	"""这边逻辑需要修改，需要把所有的IP都记录一遍，并做标记是否有效，因此需要在数据库中增加一个标记字段"""
	pass

def run_check_pool():
	"""
	运行检查IP POOL
	:return:
	"""
	ip_list = check.read_from_db()
	available_ip, unavailable_ip = validate().validate(ips=ip_list)
	check.delete_from_db(unavailable_ip)

if __name__ == '__main__':
	start = True
	while start:
		try:
			log.info('运行增加ip......')
			run_add_pool()
			log.info('进入休眠30s')
			time.sleep(10)
			log.info('运行检查数据库ip....')
			run_check_pool()
			log.info('进入休眠20s')
			time.sleep(10)
		except Exception as e:
			log.info('error:{}'.format(traceback.format_exc()))
