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
        for item in msg:
            log.info('start sending image')
            message = '国家[%s] %s %s' % (item['country'], item['name'], item['time'])
            itchat.send_msg(msg=message, toUserName=user)
            itchat.send_image(fileDir=item['img'], toUserName=user)
            try:
                log.info('delete image:%s' % item['img'])
                os.remove(path=item['img'])
            except IOError:
                log.error('delete failed')
        log.info('message has been send, waiting for next time to start')

    def getChatRoomId(self, nickname):
        # 获取群聊的username
        groupContent = itchat.get_chatrooms()
        # log.debug(groupContent)
        chatroomid = ''
        for item in groupContent:
            if item['NickName'] == nickname:
                chatroomid = item['UserName']
        print('成功获取群聊“%s”的ID：%s' % (nickname, chatroomid))
        return chatroomid


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
