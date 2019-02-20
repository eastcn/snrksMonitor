"""
east
"""
import SnrksMonitor.webspider as crawl
import SnrksMonitor.wechatnotice as notice
import yaml
import random
import time

class utils:
	@staticmethod
	def readyaml ():
		# read config from yaml document
		file = './config.yaml'
		try:
			f = open (file,'r', encoding='UTF-8')
			global configdata
			configdata = yaml.load (f)
		except IOError:
			# logging.log('open config failed')
			print ('open config failed')
		return configdata

if __name__ =='__main__':
	# 获取配置
	u = utils().readyaml()
	config_url = u['url']
	config_useragent = random.choice(u['User_Agents'])
	timeout = u['maxtimeout']
	sleeptime = u['monitortime']
	chatroomnickname = u['chatroomnickname']
	msg = ''
	data = crawl.WebSpider ()
	push = notice.wechat ()
	push.login()
	chatroomid = push.getChatRoomId(nickname=chatroomnickname)
	while True:
	# 获取网站内容和分析

		data.spider(url=config_url,useragent=config_useragent,timeout=timeout)
		msg = data.data_analysis()
		push.sendMessage(msg=msg,user=chatroomid)

		time.sleep(sleeptime) # 暂停时间
