"""
east
"""
import SnrksMonitor.webspider as crawl
import SnrksMonitor.wechatnotice as notice
import yaml
import random
import time
from SnrksMonitor.log import Logger

log = Logger().log()


class Utils:
    @staticmethod
    def readyaml():
        # read config from yaml document
        file = './config.yaml'
        try:
            f = open(file, 'r', encoding='UTF-8')
            global configdata
            configdata = yaml.load(f)
        except IOError:
            # logging.log('open config failed')
            print('open config failed')
        return configdata


if __name__ == '__main__':
    # 获取配置
    history = []
    u = Utils().readyaml()
    config_url = u['url']
    config_useragent = random.choice(u['User_Agents'])
    timeout = u['maxtimeout']
    sleeptime = u['monitortime']
    chatroomnickname = u['chatroomnickname']
    msg = ''
    data = crawl.WebSpider()
    push = notice.wechat()
    push.login()
    chatroomid = push.getChatRoomId(nickname=chatroomnickname)
    num = 1
    while True:
        # 获取网站内容和分析
        log.info('starting No.{} check'.format(num))
        try:
            data.spider(url=config_url, useragent=config_useragent, timeout=timeout)
        except TimeoutError:
            log.error('nike time out')
        msg = data.data_analysis()
        if len(msg) > 0:
            i = 1
            for item in msg:
                log.info('start downloading [{}] pictures'.format(item['sale_num']))
                data.download_imgage(url=item['img_url'], fileurl=item['img'])
                i += 1
            log.info('No.{} start pushing'.format(num))

            if num > 1:
                push.sendMessage(msg=msg, user=chatroomid)
            else:
                log.info('It is the first time to spider,so it does not push ')
                msg = {
                    'msg': "兄弟们好，你们准备好开冲了吗？",
                    'img': './img/go.jpg'
                }
                push.sendMessage(msg=msg, user=chatroomid)
        else:
            log.info('No.{} no update'.format(num))
        log.info('No.{} is over,it will sleep {} seconds'.format(num, sleeptime))
        num += 1
        time.sleep(sleeptime)  # 暂停时间


