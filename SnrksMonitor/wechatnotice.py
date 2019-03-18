"""
east
"""
import itchat
import os
from SnrksMonitor.log import Logger

log = Logger().log()


class wechat():
	def __init__(self):
		pass

	def login(self):
		itchat.auto_login(hotReload=True)

	def getFriends(self):
		friends = itchat.get_friends()
		log.debug(friends)
		return friends

	def sendMessage(self, msg, user):
		# 在群聊中发送推送并且删除图片
		if type(msg) == list:
			for item in msg:
				log.info('开始向群聊中发送消息')
				if item['shoePublishTime'] is None:
					message = '国家:[{}] [{}] '.format (item ['shoeCountry'], item ['shoeName'])
				else:
					message ="***************************\n[{}]\n国区:[{}]\n发售:[{}]\n货号:[{}]\n价格:[{}]\n抽签:[{}] \n库存:[{}]\n***************************".format(item['shoeName'],
					                            item['shoeCountry'],
					                            item['shoePublishTime'],
					                            item['shoeStyleCode'],
												item['shoePrice'],
							                    item['shoeSelectMethod'],
							                    item['shoeSize'])
				itchat.send_msg(msg=message, toUserName=user)
				itchat.send_image(fileDir=item['shoeImage'], toUserName=user)
				log.info('推送完成')
				# try: # 删除图片
				# 	log.info('delete image:%s' % item['shoeImageUrl'])
				# 	os.remove(path=item['shoeImageUrl'])
				# except IOError:
				# 	log.error('delete failed')
		elif type(msg) == str:
			log.info('请传入list')
		elif type(msg) == dict:
			log.info ('请传入list')
		else:
			itchat.send_msg(msg=msg, toUserName=user)
		log.info('message has been send, waiting for next time to start')

	def getChatRoomId(self, nickname):
		# 获取群聊的username
		groupContent = itchat.get_chatrooms()
		# log.debug(groupContent)
		chatroomid = ''
		for item in groupContent:
			if item['NickName'] == nickname:
				chatroomid = item['UserName']
		log.info('get chat room “%s” id successfully的ID：%s' % (nickname, chatroomid))
		return chatroomid

	def init(self,groupname):
		self.login()
		groupid = self.getChatRoomId(nickname=groupname)
		return groupid


# if __name__ == '__main__':
#     groupid = ''
#     msg = ''
#     try:
#         f = open('./config.yaml')
#         c = yaml.load(f)
#         groupid = c['chatroomid']
#     except IOError:
#         print('open config.yaml failed')
#     chat = wechat()
#     chat.login()
#     chat.getGroup()
# # groupid = chat.getGroup()
"""

"""
