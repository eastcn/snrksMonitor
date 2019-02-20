"""
east
"""
import itchat
import time
import yaml
import os

class wechat():
	def __init__(self):
		pass

	def login(self):
		itchat.auto_login(hotReload=True)

	def getFriends(self):
		friends = itchat.get_friends()
		print(friends)
		return friends

	def sendMessage(self,msg,user):
		# 在群聊中发送推送并且删除图片
		for item in msg:
			print('开始发送图片')
			message ='国家[%s] %s %s'%(item['country'],item['name'],item['time'])
			itchat.send_msg(msg=message,toUserName=user)
			itchat.send_image(fileDir=item['img'],toUserName=user)
			try:
				print('删除图片%s'%item['img'])
				os.remove(path=item['img'])
			except IOError:
				print('删除失败')
		print('推送结束，进入睡眠')

	def getChatRoomId(self,nickname):
		# 获取群聊的username
		groupContent = itchat.get_chatrooms()
		#print(groupContent)
		chatroomid = ''
		for item in groupContent:
			if item['NickName'] == nickname:
				chatroomid = item['UserName']
		print('成功获取群聊“%s”的ID：%s'%(nickname,chatroomid))
		return chatroomid

if __name__ == '__main__':
	groupid = ''
	msg = ''
	try:
		f = open('./config.yaml')
		c = yaml.load(f)
		groupid = c['chatroomid']
	except IOError:
		print('open config.yaml failed')
	chat = wechat ()
	chat.login()
	chat.getGroup()
	# groupid = chat.getGroup()

