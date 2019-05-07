"""
east
"""

import yaml
import requests
import re
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
        # log.debug('start download image：%s' % url)
        try:
            r = requests.get(url=url)
            with open(fileurl, 'wb') as f:
                f.write(r.content)
                f.close()
        except Exception:
            log.error('failed to download picture')
            with open('./img/go.jpg', 'wb') as fa:
                content = fa.read()
                with open(fileurl, 'wb') as fb:
                    fb.write(content)
                    fb.close()
                fa.close()
        # print('图片保存地址为：%s' % fileurl)
        # log.info('the image save in：%s' % fileurl)

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
        fileindex = 1  # 计数
        log.info("get shoes' data")
        for shoes in shoes_div:
            # shoes_name = shoes.xpath('.//h3[@class="ncss-brand u-uppercase mb-1-sm fs16-sm"]/text()')[1] # 鞋名
            shoes_link = shoes.xpath('.//a[@class="card-link d-sm-b"]/@href')  # 鞋子详情连接
            shoes_name = self.get_shoes_name(sc=shoes_link[0])
            shoes_price = self.get_shoes_price(sc=shoes_link[0], header=header, timeout=timeout)  # 价格
            shoes_img = shoes.xpath('.//img/@src')  # 图片
            shoes_sale_num = self.get_sale_num(sc=shoes_img[0])  # 货号
            fileurl = './img/shoes%s.jpg' % fileindex
            # self.download_imgage(url=shoes_img[0], fileurl=fileurl)  # 下载图片
            shoes_time = shoes.xpath('.//h6//div/text()')  # 时间
            shoes_method = self.get_shoes_method(s=shoes_time[0])  # 抽签方式
            shoes_dict = {}
            shoes_dict.update({
                'name': shoes_name,
                'img_url': shoes_img[0],
                'img': fileurl,
                'time': shoes_time,
                'country': 'cn',
                'sale_num': shoes_sale_num,
                'price': shoes_price,
                'method': shoes_method
            })
            self.datadict.append(shoes_dict)
            fileindex += 1
            log.info('get [{}] shoes'.format(shoes_sale_num))

    def data_analysis(self):
        """
        分析是否有更新
        :return: 返回更新数据
        """
        log.info('start checking whether updated or not')
        update = []
        if len(self.history) == 0:
            for shoes in self.datadict:
                self.history.append(shoes)
                update = self.history
        elif len(self.history) > 0:
            for shoes in self.datadict:
                if shoes in self.history:
                    pass
                elif shoes not in self.history:
                    update.append(shoes)
            self.history = self.datadict
            self.datadict = []

        log.info('the number of updated:%s' % len(update))
        return update

    def get_sale_num(self, sc):
        """
        :param sc:
        :return: 获取货号
        """
        pattern = re.compile('Com/.+_A')
        a = pattern.findall(sc)
        b = a[0][4:-2]
        return b

    def get_shoes_name(self, sc):
        """
        :param sc:链接url
        :return: 详细鞋名
        """
        pattern = re.compile('t/.+/')
        a = pattern.findall(sc)
        b = a[0][2:-1].replace('-', ' ')
        return b

    def get_shoes_price(self, sc, header, timeout):
        """
        获取价格
        :param sc:连接地址
        :return: 返回价格
        """
        url = 'https://www.nike.com' + sc
        price = ''
        try:
            r = requests.get(url=url, headers=header, timeout=timeout)
        except Exception:
            log.info('connect to product detail failed')
            price = '暂无'
        etree = html.etree
        s = etree.HTML(r.text)
        price = s.xpath('//div[@class="ncss-brand pb6-sm fs14-sm fs16-md"]/text()')
        return price

    def test_get_shoes_price(self):
        url = 'https://www.nike.com/cn/launch/t/air-jordan-6-retro-nrg-black-dark-concord/'
        header = {
            'User_Agents': "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
        }
        WebSpider().get_shoes_price(sc=url, header=header, timeout=30)

    def get_shoes_method(self, s):
        """
        :param s:发售时间
        :return: 抽签方式
        """
        method = ''
        if '发售' in s:
            method = '小抽签'
        else:
            method = '大抽签'
        return method
