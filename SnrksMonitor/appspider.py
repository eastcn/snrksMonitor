"""
@auther:EAST
crawl data from app
获取全部鞋子
https://api.nike.com/snkrs/content/v1/?&country=CN&language=zh-Hans&offset=0&orderBy=lastUpdated
获取entry
https://api.nike.com/launch/entries/v2
Authorization:
获取特定id鞋子
https://api.nike.com/launch/launch_views/v2?filter=productId("productid")
"""
import json
import random
import yaml
import time
from SnrksMonitor.log import Logger
from SnrksMonitor.db import db
import requests
import traceback

log = Logger().log()


class AppSpiders:
    def __init__(self):
        self.url = {
            'cn': 'https://api.nike.com/snkrs/content/v1/?&country=CN&language=zh-Hans&offset=0&orderBy=published',
            'de': 'https://api.nike.com/snkrs/content/v1/?country=DE&language=de&offset=0&orderBy=published',
            'us': 'https://api.nike.com/snkrs/content/v1/?country=US&language=en&offset=0&orderBy=published',
            'jp': 'https://api.nike.com/snkrs/content/v1/?country=JP&language=ja&offset=0&orderBy=published'
        }

        self.entry = 'https://api.nike.com/launch/entries/v2'
        useragent = random.choice(self.readyaml()['User_Agents'])
        # auth = self.readyaml()['auth']
        self.headers = {
            'User_Agents': useragent
            # 'Authorization': auth
        }
        self.db = db()
        self.country = ['cn', 'us', 'jp']

    def readyaml(self):
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

    def spiderDate(self, country):
        """
        通过snrks的首页接口获取到首页最新放送的鞋子数据
        名字+颜色 图片 货号 发售方式 价格 库存码数 发售时间
        :return: 返回出来一个数组，包含前50条的鞋子数据
        """
        header = {
            'User-Agent': random.choice(self.readyaml()['User_Agents'])
        }
        proxy = {
        }
        log.info('最新的数据获取中...')
        url = self.url[country]
        global shoes
        try:
            responce = requests.get(url, headers=header)
            responceJson = json.loads(responce.text)
            shoes = responceJson['threads']
        except Exception as e:
            ex = traceback.format_exc()
            isSuccess = False
            failedNum = 1
            while isSuccess == False:
                log.info('获取{}接口失败，正在重试第{}次......'.format(country, failedNum))
                log.debug('以下为详细错误：{}'.format(ex))
                responce = requests.get(url, headers=self.headers)
                responceJson = json.loads(responce.text)
                if 'threads' in responceJson.keys():
                    shoes = responceJson['threads']
                    log.info('重试成功，正在恢复')
                    isSuccess = True
                elif failedNum == 30:
                    shoes = []
                    break
                else:
                    failedNum += 1
        shoesData = []
        for shoe in shoes:
            """ 从接口中获取到一双鞋子的数据 包括pass """
            product = shoe['product']
            shoeStyle = product['style']
            if shoeStyle == '999999':
                shoeDict = {
                    'id': None,
                    'shoeName': shoe['name'],
                    'shoeImageUrl': shoe['imageUrl'],
                    'shoeImage': None,
                    'shoeColor': '',
                    'shoeStyleCode': '',
                    'shoeSelectMethod': '',
                    'shoePrice': '',
                    'shoeSize': '',
                    'shoePublishTime': '',
                    'shoeCountry': country,
                    'shoeUpdateTime': ''
                }
            else:
                shoeSize = ''
                for sku in product['skus']:
                    shoeSize = '{}|{}'.format(shoeSize, sku['localizedSize'])
                try:
                    selector = product['selectionEngine']
                except KeyError:
                    selector = None
                t = product['startSellDate'][:19].replace('T', ' ')
                shoeTime = self.changeTime(t=t, c=country)
                shoeDict = {
                    'id': None,
                    'shoeName': shoe['name'],
                    'shoeColor': product['colorDescription'],
                    'shoeImageUrl': product['imageUrl'],
                    'shoeImage': None,
                    'shoeStyleCode': "{}-{}".format(product['style'], product['colorCode']),
                    'shoeSelectMethod': selector,
                    'shoePrice': product['price']['msrp'],
                    'shoeSize': shoeSize,
                    'shoePublishTime': shoeTime,
                    'shoeCountry': country,
                    'shoeUpdateTime': shoe['lastUpdatedTime']
                }
            shoesData.append(shoeDict)
        log.info('最新的数据获取完成')
        return shoesData

    def getNewShoesData(self):
        """
        整合四个区的获取到的新数据
        :return:
        """
        allCountrtyShoesData = []
        for country in self.country:
            data = self.spiderDate(country=country)
            allCountrtyShoesData = data + allCountrtyShoesData
        return allCountrtyShoesData

    def changeTime(self, t, c):
        """
        返回根据不同区转换后的时间
        :param t:
        :param c:
        :return:
        """
        timeArray = time.strptime(t, "%Y-%m-%d %H:%M:%S")
        timestamp = int(time.mktime(timeArray))
        global resulttime
        if c == 'cn' or 'us':
            timestamp_cn = timestamp + 28800
            timeArray_cn = time.localtime(timestamp_cn)
            resulttime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray_cn)
        elif c == 'jp':
            timestamp_jp = timestamp + 32400
            timeArray_jp = time.localtime(timestamp_jp)
            resulttime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray_jp)
        elif c == 'de':
            timestamp_cn = timestamp + 21600
            timeArray_cn = time.localtime(timestamp_cn)
            resulttime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray_cn)
        return resulttime

    def updateCheck(self, data):
        """
        用来检查是否有数据更新
        :param data: 传入需要进行对比的数据
        :return: 返回一个更新的数组和是否更新，数组中存的是鞋子的货号
        """
        log.info('数据更新确认中...')
        fetchSql = """SELECT shoeStyleCode,shoename,shoeCountry,shoeUpdateTime,create_time FROM shoes"""
        OldData = self.db.fetchData(sql=fetchSql, c=None)
        if len(OldData) == 0:
            self.db.updateShoesTable(data=data)
            message = {
                'isUpdate': False,
                'data': 'no data'
            }
        else:
            CodeData_cn, NameData_cn = self.getCountryData(country='cn')
            CodeData_us, NameData_us = self.getCountryData(country='us')
            CodeData_de, NameData_de = self.getCountryData(country='de')
            CodeData_jp, NameData_jp = self.getCountryData(country='jp')
            isUpdate = False
            updateData = []
            # 获取到的新数据按照国区分别进行更新检查
            for newdata in data:
                if newdata['shoeCountry'] == 'cn':
                    if newdata['shoeStyleCode'] not in CodeData_cn or newdata['shoeName'] not in NameData_cn:
                        updateData.append(newdata)
                        # 把更新的鞋子的图片下载到本地并把url改为本地url
                        newdata['shoeImage'] = self.download_imgage(url=newdata['shoeImageUrl'],
                                                                    filename=newdata['shoeStyleCode'])
                        newdata['id'] = None
                        isUpdate = True
                    else:
                        # 判断鞋子的last更新时间是否比存在数据库中的更新时间大，以下三国一样的
                        pass
                elif newdata['shoeCountry'] == 'us':
                    if newdata['shoeStyleCode'] not in CodeData_us or newdata['shoeName'] not in NameData_us:
                        updateData.append(newdata)
                        # 把更新的鞋子的图片下载到本地并把url改为本地url
                        newdata['shoeImage'] = self.download_imgage(url=newdata['shoeImageUrl'],
                                                                    filename=newdata['shoeStyleCode'])
                        newdata['id'] = None
                        isUpdate = True
                elif newdata['shoeCountry'] == 'de':
                    if newdata['shoeStyleCode'] not in CodeData_de or newdata['shoeName'] not in NameData_de:
                        updateData.append(newdata)
                        # 把更新的鞋子的图片下载到本地并把url改为本地url
                        newdata['shoeImage'] = self.download_imgage(url=newdata['shoeImageUrl'],
                                                                    filename=newdata['shoeStyleCode'])
                        newdata['id'] = None
                        isUpdate = True
                elif newdata['shoeCountry'] == 'jp':
                    if newdata['shoeStyleCode'] not in CodeData_jp or newdata['shoeName'] not in NameData_jp:
                        updateData.append(newdata)
                        # 把更新的鞋子的图片下载到本地并把url改为本地url
                        newdata['shoeImage'] = self.download_imgage(url=newdata['shoeImageUrl'],
                                                                    filename=newdata['shoeStyleCode'])
                        newdata['id'] = None
                        isUpdate = True
            message = {
                'isUpdate': isUpdate,
                'data': updateData
            }
            log.info('数据更新确认完成')
        return message

    def getCountryData(self, country):
        """
        用于获取数据库中特定国家的数据
        :param country:
        :return:
        """
        fetchsql = """SELECT shoeStyleCode,shoename FROM shoes where shoeCountry ='{}' """.format(country)
        countryData = self.db.fetchData(sql=fetchsql, c=None)
        CodeData = []
        NameData = []
        for data in countryData:
            CodeData.append(data[0])
            NameData.append(data[1])
        return CodeData, NameData

    def insertToDb(self, data):
        log.info('向更新表中插入数据中...')
        insertSql = """INSERT INTO "update" values (?,?,?,?,?,?,?,?,?,?,?)"""
        insertData = []
        for item in data:
            dataturple = (
                item['id'],
                item['shoeName'],
                item['shoeColor'],
                item['shoeImageUrl'],
                item['shoeImage'],
                item['shoeStyleCode'],
                item['shoeSelectMethod'],
                item['shoePrice'],
                item['shoeSize'],
                item['shoePublishTime'],
                item['shoeCountry']
            )
            insertData.append(dataturple)
        self.db.insertData(sql=insertSql, d=insertData, path=None)
        log.info('向更新表中插入数据结束')

    def initDB(self):
        deleteSql = """DELETE FROM "update" where id < 100000"""
        self.db.deleteData(sql=deleteSql)
        log.info('初始化更新表完成...')

    def download_imgage(self, url, filename):
        """
        用于下载图片，并返回图片url
        :param url: 图片的网络地址
        :param filename: 需要存放在本地的图片名字
        :return: 返回本地的图片地址
        """
        log.debug('start download image：%s' % filename)
        fileurl = './img/{}.jpg'.format(filename)
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
        return fileurl


if __name__ == '__main__':
    shoesdata = AppSpiders()  # 实例化鞋子爬虫的类
    shoesdata.initDB()  # 初始化
    NewData = shoesdata.spiderDate()
    result = shoesdata.updateCheck(data=NewData)
    print(result)
    if result['isUpdate'] is True:
        updateData = result['data']
        shoesdata.insertToDb(data=updateData)
