"""
验证数据库中的IP是否可用，不可用则删除
"""
import traceback
from log import Logger
from SnrksMonitor.db import db


log = Logger().log()


class CheckFromDb:
	def __init__(self):
		self.db = db()

	def read_from_db(self):
		"""
		从数据库中读取数据
		:return:
		"""
		fetchSql = """SELECT * From 'ips'"""
		db_data = self.db.fetchData(sql=fetchSql,c=None)
		ip_list = []
		for data in db_data:
			ip_dict = {
				'id': data[0],
				'ip': data[2],
				'http': data[1],
				'port': data[3]
			}
			ip_list.append(ip_dict)
		return ip_list

	def delete_from_db(self,list):
		"""
		从数据库中删除数据
		:return:
		"""
		id_list = []
		for ip in list:
			id_list.append(ip['id'])
		ids = tuple(id_list)
		self.db.deleteFromIpTable(ids=ids)

	def test_delete_from_db(self):
		ip_list = [{'id':1,'ip': '36.26.220.69', 'port': '9999', 'http': 'https'},
		           {'id':2,'ip': '116.209.54.75', 'port': '9999', 'http': 'https'},
		           {'id':3,'ip': '116.209.53.242', 'port': '9999', 'http': 'https'}]
		self.delete_from_db(list=ip_list)

	def inserte_into_db(self,list):
		"""
		将ip插入数据库
		:param list:
		:return:
		"""
		for ip in list:
			data = [(None, ip['http'], ip['ip'], ip['port'])]
			log.info ('开始插入数据库')
			try:
				self.db.insertIntoIpTable (data=data)
			except Exception as e:
				log.info ('{}'.format (traceback.format_exc ()))
	def test_inserte_into_db(self):
		ip_list = [{'id': 1, 'ip': '36.26.220.69', 'port': '9999', 'http': 'https'},
		           {'id': 2, 'ip': '116.209.54.75', 'port': '9999', 'http': 'https'},
		           {'id': 3, 'ip': '116.209.53.242', 'port': '9999', 'http': 'https'}]
		self.inserte_into_db(list=ip_list)

	def if_update(self,list):
		"""
		判断跟数据库中对比是否更新
		:param list:
		:return:
		"""
		oldData = self.read_from_db()
		newData = list
		oldIPs= []
		newIPs = []
		isUpdate = False
		for oldip in oldData:
			oldIPs.append(oldip['ip'])

		for newip in newData:
			if newip['ip'] not in oldIPs:
				newIPs.append(newip)
				isUpdate = True
		updata_dict = {
			'isupdate' : isUpdate,
			'data': newIPs
		}
		return updata_dict

	def test_if_update(self):
		ip_list = [{'id': 1, 'ip': '36.26.220.691', 'port': '9999', 'http': 'https'},
		           {'id': 2, 'ip': '116.209.54.752', 'port': '9999', 'http': 'https'},
		           {'id': 3, 'ip': '116.209.53.242', 'port': '9999', 'http': 'https'}]
		a = self.if_update(list=ip_list)
		print(a)

if __name__ == '__main__':
	# CheckFromDb().test_delete_from_db()
	CheckFromDb().test_if_update()
