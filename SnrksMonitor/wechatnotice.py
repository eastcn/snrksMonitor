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
                log.info('start sending image')
                message = '国家[%s] %s %s 货号[%s] 价格[%s] 抽签方式[%s]' % (item['country'], item['name'], item['time'],
                                                                   item['sale_num'], item['price'], item['method'])
                itchat.send_msg(msg=message, toUserName=user)
                itchat.send_image(fileDir=item['img'], toUserName=user)
                try:
                    log.info('delete image:%s' % item['img'])
                    os.remove(path=item['img'])
                except IOError:
                    log.error('delete failed')
        elif type(msg) == str:
            itchat.send_msg(msg=msg, toUserName=user)
        elif type(msg) == dict:
            itchat.send_msg(msg=msg['msg'], toUserName=user)
            itchat.send_image(fileDir=msg['img'], toUserName=user)
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
