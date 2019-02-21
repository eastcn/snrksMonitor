"""
east
"""

import yaml
import requests
from lxml import html
from SnrksMonitor.log import Logger


# create a static dict to save history data

log = Logger().log()


class WebSpider:

    def __init__(self):
        self.datadict = []
        self.history = []

    @staticmethod
    def readyaml():
        # read config from yaml document
        file = './config.yaml'
        try:
            f = open(file)
            global configdata
            configdata = yaml.load(f)
        except IOError:
            # print('open config failed')
            log.error('open config failed')
        return configdata

    def download_imgage(self, url, fileurl):
        log.info('start download image：%s' % url)
        r = requests.get(url=url)
        with open(fileurl, 'wb') as f:
            f.write(r.content)
        # print('图片保存地址为：%s' % fileurl)
        log.info('the image save in：%s' % fileurl)
        f.close()

    def spider(self, url, useragent, timeout):
        # 爬取snrks网站内容
        # config = self.readyaml()
        # url = config['url']
        # useragent = random.choice(config['User_Agents'])
        header = {
            'User_Agents': useragent
        }
        # logging.log('start spiders')
        # print('开始请求nike网站')
        log.info('start connect to nike')
        r = requests.get(url=url, headers=header, timeout=timeout)
        etree = html.etree
        s = etree.HTML(r.text)
        # 以下为对nike网站的分析
        log.info("start analysis nike'website")
        shoes_div = s.xpath('//figure[@class="d-md-h ncss-col-sm-12 va-sm-t pb0-sm prl0-sm"]')
        fileindex = 0
        for shoes in shoes_div:
            self.datadict = []
            shoes_name = shoes.xpath('.//h3[@class="ncss-brand u-uppercase mb-1-sm fs16-sm"]/text()')[1]
            shoes_img = shoes.xpath('.//img/@src')
            fileurl = './img/shoes%s.jpg' % fileindex
            self.download_imgage(url=shoes_img[0], fileurl=fileurl)
            shoes_time = shoes.xpath('.//h6//div/text()')
            shoes_dict = {}
            shoes_dict.update({
                'name': shoes_name,
                'img': fileurl,
                'time': shoes_time,
                'country': 'cn'
            })
            self.datadict.append(shoes_dict)
            fileindex += 1

    def data_analysis(self, update):
        # data check
        # print('开始记录是否有更新')
        log.info('start checking whether updated or not')
        if len(self.history) == 0:
            for shoes in self.datadict:
                self.history.append(shoes)
        elif len(self.history) > 0:
            for shoes in self.datadict:
                if shoes in self.history:
                    pass
                elif shoes not in self.history:
                    update.append(shoes)

        log.info('the number of updated:%s' % len(update))
        return update

# if __name__ == '__main__':
#     run = WebSpider()
#     run.spider()
#     print(run.data_analysis())
