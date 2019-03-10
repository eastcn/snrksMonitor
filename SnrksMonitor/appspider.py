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
import random
import yaml
from SnrksMonitor.log import Logger
from SnrksMonitor.db import db
import requests

log = Logger().log()


class AppSpiders:
	def __init__ (self):
		self.url = 'https://api.nike.com/snkrs/content/v1/?&country=CN&language=zh-Hans&offset=0&orderBy=published'
		self.entry = 'https://api.nike.com/launch/entries/v2'
		useragent = random.choice (self.readyaml () ['User_Agents'])
		# auth = Utils.readyaml()['auth']
		self.headers = {
			'User_Agents': useragent
			# 'Authorization': auth
		}
		self.db = db ()

	def readyaml (self):
		# read config from yaml document
		file = './config.yaml'
		try:
			f = open (file, 'r', encoding='UTF-8')
			global configdata
			configdata = yaml.load (f)
		except IOError:
			# logging.log('open config failed')
			print ('open config failed')
		return configdata


	def spiderDate (self):
		"""
        通过snrks的首页接口获取到首页最新放送的鞋子数据
        名字+颜色 图片 货号 发售方式 价格 库存码数 发售时间
        :return: 返回出来一个数组，包含前50条的鞋子数据
        """
		log.info('最新的数据获取中...')
		try:
			responce = requests.get (self.url, headers=self.headers)
			responceJson = json.loads (responce.text)
			shoes = responceJson ['threads']
		except (KeyError,TimeoutError):
			isSuccess = False
			failedNum = 1
			while isSuccess == False:
				log.info('获取接口失败，正在重试第{}次......'.format(failedNum))
				responce = requests.get (self.url, headers=self.headers)
				responceJson = json.loads (responce.text)
				if 'threads' in responceJson.keys():
					shoes = responceJson ['threads']
					log.info('重试成功，正在恢复')
					isSuccess = True

				else:
					failedNum += 1

		shoesData = []
		n = 1
		for shoe in shoes:
			""" 从接口中获取到一双鞋子的数据 包括pass """
			product = shoe ['product']
			shoeStyle = product ['style']
			if shoeStyle == '999999':
				shoeDict = {
					'id'              : n,
					'shoeName'        : shoe ['name'],
					'shoeImageUrl'    : shoe ['imageUrl'],
					'shoeImage'       : None,
					'shoeColor'       : '',
					'shoeStyleCode'   : '',
					'shoeSelectMethod': '',
					'shoePrice'       : '',
					'shoeSize'        : '',
					'shoePublishTime' : ''
				}
			else:
				shoeSize = ''
				for sku in product ['skus']:
					shoeSize = '{}|{}'.format (shoeSize, sku ['localizedSize'])
				try:
					selector = product ['selectionEngine']
				except KeyError:
					selector = None
				shoeDict = {
					'id'              : n,
					'shoeName'        : shoe ['name'],
					'shoeColor'       : product ['colorDescription'],
					'shoeImageUrl'    : product ['imageUrl'],
					'shoeImage'       : None,
					'shoeStyleCode'   : "{}-{}".format (product ['style'], product ['colorCode']),
					'shoeSelectMethod': selector,
					'shoePrice'       : product ['price'] ['msrp'],
					'shoeSize'        : shoeSize,
					'shoePublishTime' : product ['startSellDate'] [:20].replace ('T', ' ')
				}
			n += 1
			shoesData.append (shoeDict)
		log.info('最新的数据获取完成')
		return shoesData

	def updateCheck (self,data):
		"""
		用来检查是否有数据更新
		:param data: 传入需要进行对比的数据
		:return: 返回一个更新的数组和是否更新，数组中存的是鞋子的货号
		"""
		log.info('数据更新确认中...')
		fetchSql = """SELECT shoeStyleCode FROM shoes"""
		OldData = self.db.fetchData(sql=fetchSql,c=None)
		if len(OldData) == 0:
			self.db.updateShoesTable(data=data)
			message = {
				'isUpdate': False,
				'data'    : 'no data'
			}
		else:
			OldDataList = []
			for olddata in OldData:
				OldDataList.append(olddata[0])
			isUpdate = False
			updateData = []
			for newdata in data:
				if newdata['shoeStyleCode'] not in OldDataList:
					updateData.append(newdata)
					# 把更新的鞋子的图片下载到本地并把url改为本地url
					newdata['shoeImage'] = self.download_imgage(url=newdata['shoeImageUrl'],filename=newdata['shoeStyleCode'])
					newdata['id'] = None
					isUpdate = True
			message ={
				'isUpdate': isUpdate,
				'data': updateData
			}
			log.info('数据更新确认完成')
		return message


	def insertToDb(self,data):
		log.info('向更新表中插入数据中...')
		insertSql = """INSERT INTO "update" values (?,?,?,?,?,?,?,?,?,?)"""
		insertData = []
		for item in data:
			dataturple = (
				item['id'],
				item['shoeName'],
				item['shoeColor'],
				item['shoeImageUrl'],
				item['shoeImage'],
				item['shoeStyleCode'],
				item['shoeSelectMethod'],
				item['shoePrice'],
				item['shoeSize'],
				item['shoePublishTime']
			)
			insertData.append(dataturple)
		self.db.insertData(sql=insertSql,d=insertData)
		log.info('向更新表中插入数据结束')

	def initDB(self):
		deleteSql = """DELETE FROM "update" where id < 50"""
		self.db.deleteData(sql=deleteSql)
		log.info('初始化更新表完成...')


	def download_imgage (self, url, filename):
		"""
		用于下载图片，并返回图片url
		:param url: 图片的网络地址
		:param filename: 需要存放在本地的图片名字
		:return: 返回本地的图片地址
		"""
		log.debug('start download image：%s' % filename)
		fileurl = './img/{}.jpg'.format(filename)
		try:
			r = requests.get (url=url)
			with open (fileurl, 'wb') as f:
				f.write (r.content)
				f.close ()
		except Exception:
			log.error ('failed to download picture')
			with open ('./img/go.jpg', 'wb') as fa:
				content = fa.read ()
				with open (fileurl, 'wb') as fb:
					fb.write (content)
					fb.close ()
				fa.close ()
		return fileurl

if __name__ == '__main__':
	shoesdata = AppSpiders () # 实例化鞋子爬虫的类
	shoesdata.initDB() # 初始化
	NewData = shoesdata.spiderDate()
	result = shoesdata.updateCheck(data=NewData)
	print(result)
	if result['isUpdate'] is True:
		updateData = result['data']
		shoesdata.insertToDb(data=updateData)



