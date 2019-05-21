"""
author: hefeng
date: 2019.5.20
function: 运行多线程爬虫
"""
from apscheduler.schedulers.background import BlockingScheduler
import threading
from SnrksMonitor.log import Logger
from SnrksMonitor.appspider import AppSpiders
from SnrksMonitor.db import db as database
from SnrksMonitor.new_ios_push import PushToIos

log = Logger().log()
scheduler = BlockingScheduler()


class RunSpider:
    def __init__(self):
        self.message = "1"
        self.spider = AppSpiders()
        self.db = database()
        self.data = []
        self.district = self.spider.readyaml()['country']
        self.Push = PushToIos()

    def get_data(self, district):
        """
        获取最新的数据
        :return:最新的数据
        """
        log.info("开始爬取最新的数据")
        origin_data = self.spider.spiderDate(district)
        # print(origin_data)
        data = self.spider.updateCheck(origin_data)
        flag = data['isUpdate']
        if flag is True:
            self.data.append(data)
            # print(data)
        else:
            log.info("本次没有更新")

    def insert_db(self):
        """
        插入数据库
        :return:
        """
        log.info("重新数据库初始化...")
        self.spider.initDB()
        for item in self.data:
            self.db.updateShoesTable(data=item["data"])

    def push(self):
        """
        推送
        :return:
        """
        log.info("推送中...")
        if len(self.data) == 0:
            self.Push.push('test empty')
        else:
            for item in self.data:
                for shoe_data in item["data"]:
                    msg_1 = f"[{shoe_data['shoeCountry']}] [{shoe_data['shoeSelectMethod']}] 时间:[{shoe_data['shoePublishTime']}]"
                    msg_2 = f"{shoe_data['shoeName']} {shoe_data['shoeStyleCode']}"
                    url_key = f"?url={shoe_data['shoeImageUrl']}"
                    self.Push.push(message=msg_1+msg_2+url_key)

    def init_data(self):
        """
        初始化self中的data数据
        :return:
        """
        self.data = []


def run_spider():
    run = RunSpider()
    spider_thread_pool = []
    for d in run.district:
        t = threading.Thread(target=run.get_data, args=([d]))
        spider_thread_pool.append(t)
    for t in spider_thread_pool:
        t.start()
    for t_j in spider_thread_pool:
        t_j.join()
    if len(run.data) > 0:
        run.insert_db()
        run.push()
    run.init_data()


if __name__ == "__main__":
    print('start')
    run_spider()
    scheduler.add_job(run_spider, "interval", seconds=120, max_instances=5)
    scheduler.start()
