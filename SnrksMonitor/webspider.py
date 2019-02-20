"""
east
"""


import yaml
import random
from lxml import html
import requests

# create a static dict to save history data
history = []


class WebSpider:

    def __init__(self):
        self.datadict = []

    @staticmethod
    def readyaml():
        # read config from yaml document
        file = './config.yaml'
        try:
            f = open(file)
            global configdata
            configdata = yaml.load(f)
        except IOError:
            # logging.log('open config failed')
            print('open config failed')
        return configdata

    def download_imgage(self,url,fileurl):
        print ('下载图片：%s'%url)
        r = requests.get(url=url)
        with open(fileurl,'wb') as f:
            f.write(r.content)
        print('图片保存地址为：%s'%fileurl)
        f.close()

    def spider(self,url,useragent,timeout):
        # 爬取snrks网站内容
        # config = self.readyaml()
        # url = config['url']
        # useragent = random.choice(config['User_Agents'])
        header = {
            'User_Agents':useragent
        }
        # logging.log('start spiders')
        print('开始请求nike网站')
        r = requests.get(url=url, headers=header,timeout=timeout)
        etree = html.etree
        s = etree.HTML(r.text)
        # 以下为对nike网站的分析
        shoes_div = s.xpath('//figure[@class="d-md-h ncss-col-sm-12 va-sm-t pb0-sm prl0-sm"]')
        fileindex = 0
        for shoes in shoes_div:
            shoes_name = shoes.xpath('.//h3[@class="ncss-brand u-uppercase mb-1-sm fs16-sm"]/text()')[1]
            shoes_img = shoes.xpath('.//img/@src')
            fileurl = './img/shoes%s.jpg'%fileindex
            self.download_imgage(url=shoes_img[0],fileurl=fileurl)
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

    def data_analysis(self):
        # data check
        update = []
        print('开始记录是否有更新')
        if history is None:
            for shoes in self.datadict:
                history.append(shoes)
        elif history is not None:
            for shoes in self.datadict:
                if shoes in history:
                    pass
                elif shoes not in history:
                    update.append(shoes)
        print('更新内容数量为%s'%len(update))
        return update


# if __name__ == '__main__':
#     run = WebSpider()
#     run.spider()
#     print(run.data_analysis())

