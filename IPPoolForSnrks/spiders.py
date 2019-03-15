"""
从国内几个免费的代理网站上爬取免费代理
"""
import random
import requests
from lxml import etree
from utils import utils

class proxyspider:
	def __init__(self):
		self.config = utils().readconfig()
		self.headers = {
			'User-Agent': random.choice(self.config['User_Agents'])
		}


	def spiderFromXici(self,url='https://www.xicidaili.com/nn/'):
		IPPool = []
		for i in range(1):
			#a = config()
			page = 1
			user_agent = self
			headers = {
				'User-Agent' : user_agent
			}
			Url = url + str(page)
			r = requests.get(url=Url,headers=self.headers)
			selector = etree.HTML(r.text)
			tr = selector.xpath('//tr') #选取页面中的所有tr标签
			for t in range(len(tr)):
				if t >= 1:
					ippool={
						'ip' : '',
						'port':'',
						'http':''
					}
					ippool['ip'] = tr[t].xpath ('./td[2]/text()')[0]
					ippool['port'] = tr[t].xpath ('./td[3]/text()')[0]
					temp = tr[t].xpath('./td[6]/text()')[0]
					if temp == 'HTTP':
						ippool ['http'] = 'http'
					elif temp == 'HTTPS':
						ippool ['http'] = 'https'
					IPPool.append(ippool)
		return IPPool




if __name__ == '__main__':
	for ip in proxyspider().spiderFromXici():
		print(ip)

