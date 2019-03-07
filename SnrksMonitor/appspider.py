"""
@auther:EAST
crawl data from app
获取全部鞋子
https://api.nike.com/snkrs/content/v1/?&country=CN&language=zh-Hans&offset=0&orderBy=lastUpdated
获取entry
https://api.nike.com/launch/entries/v2
Authorization:
获取特定id鞋子
https://api.nike.com/launch/launch_views/v2?filter=productId("productid")
"""
import json
import time
import random
from SnrksMonitor.db import db
from sqlite3.dbapi2 import Cursor

import requests
from SnrksMonitor.main import Utils


class AppSpiders:
	def __init__ (self):
		self.url = 'https://api.nike.com/snkrs/content/v1/?&country=CN&language=zh-Hans&offset=0&orderBy=published'
		self.entry = 'https://api.nike.com/launch/entries/v2'
		useragent = random.choice (Utils.readyaml () ['User_Agents'])
		auth = Utils.readyaml()['auth']
		self.headers = {
			'User_Agents': useragent,
			'Authorization': auth
		}

	def spiderDate (self):
		"""
		通过snrks的首页接口获取到首页最新放送的鞋子数据
		名字+颜色 图片 货号 发售方式 价格 库存码数 发售时间
		:return: 返回出来一个数组，包含前50条的鞋子数据
		"""
		responce = requests.get (self.url, headers=self.headers)
		responceJson = json.loads(responce.text)
		shoes = responceJson['threads']
		shoesData = []
		for shoe in shoes:
			""" 从接口中获取到一双鞋子的数据 包括pass """
			product = shoe['product']
			shoeStyle = product['style']
			if shoeStyle == 999999:
				shoeDict = {
					'shoeName': shoe['name'],
					'shoeImageUrl' : shoe['imageUrl']
				}
			else:
				shoeSize = []
				for sku in product ['skus']:
					shoeSize.append (sku ['localizedSize'])
				shoeDict = {
					'shoeName'        : shoe ['name'],
					'shoeColor'       : product ['colorDescription'],
					'shoeImageUrl'    : product ['imageUrl'],
					'shoeStyleCode'   : f"{product['style']}-{product['colorCode']}",
					'shoeSelectMethod': product ['selectionEngine'],
					'shoePrice'       : product ['price'] ['msrp'],
					'shoeSize'        : shoeSize,
					'shoePublishTime' : product ['startSellDate']
				}
			shoesData.append (shoeDict)
		return shoesData


if __name__ == '__main__':
	AppSpiders().spiderDate()



