"""
运行脚本
"""

import SnrksMonitor.wechatnotice as notice
import time
import yaml
from SnrksMonitor.log import Logger
from SnrksMonitor.appspider import AppSpiders
from SnrksMonitor.db import db as database

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


def run():
    log.info('East SnrksMonitor is starting')
    # 从配置中获取超时，爬虫间隔，微信群组名字
    u = Utils().readyaml()
    # timeout = u ['maxtimeout']
    sleeptime = u['monitortime']
    chatroomnickname = u['chatroomnickname']

    # 登录微信 并返回群组id
    # push = notice.wechat ()
    # chatroomid = push.init (groupname=chatroomnickname)
    num = 1

    # 实例化爬虫类
    shoesdata = AppSpiders()
    db = database()
    while True:
        log.info('第{}次开始'.format(num))
        NewData = shoesdata.getNewShoesData()  # 获取到最新的数据
        result = shoesdata.updateCheck(data=NewData)  # 获取到是否有更新和更新数据
        log.info('第{}次是否有更新：{}'.format(num, result['isUpdate']))
        # 如果有更新则对更新表进行操作，并发送推送
        if result['isUpdate'] is True:
            # 初始化鞋子，删除更新表
            shoesdata.initDB()  # 初始化
            # 对更新表进行操作
            updateData = result['data']
            shoesdata.insertToDb(data=updateData)
            # 给微信群发送推送
            updateShoesCodeList = []
            for updatedata in updateData:
                updateShoesCodeList.append(updatedata['shoeStyleCode'])
            log.info('第{}次更新的货号：{}'.format(num, updateShoesCodeList))
            # push.sendMessage(user=chatroomid, msg=updateData)
            # 把有更新的数据插入鞋子表
            db.updateShoesTable(data=updateData)
        else:
            # 是否需要操作？
            log.info('第{}次没有更新，进入暂停'.format(num))
        log.info('第{}次结束'.format(num))
        num += 1
        time.sleep(sleeptime)  # 暂停时间
