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

    def spider(self):
        # 爬取snrks网站内容
        config = self.readyaml()
        url = config['url']
        useragent = random.choice(config['User_Agents'])
        header = {
            'User_Agents':useragent
        }
        print(header)
        # logging.log('start spiders')
        r = requests.get(url=url, headers=header)
        etree = html.etree
        s = etree.HTML(r.text)
        # 以下为对nike网站的分析
        shoes_div = s.xpath('//figure[@class="d-md-h ncss-col-sm-12 va-sm-t pb0-sm prl0-sm"]')
        for shoes in shoes_div:
            shoes_name = shoes.xpath('.//h3[@class="ncss-brand u-uppercase mb-1-sm fs16-sm"].text')
            print(shoes_name)
            # shoes_style = shoes.xpath('.//div[@class="figcaption-content"]//h6')
            shoes_img = shoes.xpath('.//img/@src')
            print(shoes_img)
            shoes_time = shoes.xpath('.//h6//div')
            shoes_dict = {}
            shoes_dict.update({
                'name': shoes_name,
                'img': shoes_img,
                'time': shoes_time,
                'country': 'cn'
            })
            self.datadict.append(shoes_dict)

    def data_analysis(self):
        # data check
        update = []
        if history[0] is None:
            for shoes in self.datadict:
                history.append(shoes)
        elif history[0] is not None:
            for shoes in self.datadict:
                if shoes in history:
                    pass
                elif shoes not in history:
                    update.append(shoes)
        return update


if __name__ == '__main__':
    run = WebSpider()
    run.spider()
    run.data_analysis()

