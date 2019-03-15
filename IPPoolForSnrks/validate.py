"""
用于验证ip代理是否可用
"""
from log import Logger
import json
import requests
import datetime
import traceback
from SnrksMonitor.db import db

log = Logger().log()


class validate:
	def __init__(self):
		self.checkurl= 'http://httpbin.org/get'
		self.db = db()
	def validate(self,ips):
		"""
		验证是什么代理，统计代理数量，插入数据库
		:param ips: 代理ip列表
		:return: None
		"""
		available_ips = []
		unavailable_ips = []
		for ip in ips:
			log.info(f'开始验证代理{ip ["http"]}：{ip["ip"]}:{ip["port"]}')
			ip_port = f'{ip["ip"]}:{ip["port"]}'
			proxy = {ip ['http']: ip_port}
			time = datetime.datetime.now ().now ().strftime ('%Y-%m-%d %H:%M:%S')
			try:
				r = requests.get (url=self.checkurl, proxies=proxy, timeout=1)
				if r.status_code == 200:
					result = json.loads (r.text)
					ip_proxy = ip ['ip']
					ip_v = result ['origin']
					headers = result ['headers']
					proxy_connection = headers.get ('Proxy-Connection', None)
					# 判断是否为普通匿名，透明，或者高级匿名，记录普通匿名和高级匿名到数据库
					if proxy_connection:
						log.info (f"{time} success: {ip ['http']}://{ip ['ip']}:{ip ['port']} ----普通匿名")
						available_ips.append(ip)
					elif ',' in ip_v:
						log.info (f"{time} success: {ip ['http']}://{ip ['ip']}:{ip ['port']} ----透明")
						unavailable_ips.append(ip)
					else:
						log.info (f"{time} success: {ip ['http']}://{ip ['ip']}:{ip ['port']} ----高级匿名")
						available_ips.append (ip)

				else:
					log.info (f"{time} failed: {ip ['http']}://{ip ['ip']}:{ip ['port']} ----无效代理")
					unavailable_ips.append (ip)
			except Exception as e:
				log.info ('error:'+ repr(e))
				log.info (f"{time} error: {ip ['http']}://{ip ['ip']}:{ip ['port']} ----无效代理")
				unavailable_ips.append (ip)

		return available_ips,unavailable_ips

	def test_validate(self):
		ip_list = [{'ip': '36.26.220.69', 'port': '9999', 'http': 'https'},
		           {'ip': '116.209.54.75', 'port': '9999', 'http': 'https'},
		           {'ip': '116.209.53.242', 'port': '9999', 'http': 'https'}]
		self.validate(ip_list)


if __name__ == "__main__":
	validate().test_validate()
