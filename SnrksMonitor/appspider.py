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
from SnrksMonitor.db import db
import requests
from SnrksMonitor.main import Utils


class AppSpiders:
    def __init__(self):
        self.url = 'https://api.nike.com/snkrs/content/v1/?&country=CN&language=zh-Hans&offset=0&orderBy=published'
        self.entry = 'https://api.nike.com/launch/entries/v2'
        useragent = random.choice(Utils.readyaml()['User_Agents'])
        #auth = Utils.readyaml()['auth']
        self.headers = {
            'User_Agents': useragent
            #'Authorization': auth
        }

    def spiderDate(self):
        """
        通过snrks的首页接口获取到首页最新放送的鞋子数据
        名字+颜色 图片 货号 发售方式 价格 库存码数 发售时间
        :return: 返回出来一个数组，包含前50条的鞋子数据
        """
        responce = requests.get(self.url, headers=self.headers)
        responceJson = json.loads(responce.text)
        shoes = responceJson['threads']
        shoesData = []
        n = 1
        for shoe in shoes:
            """ 从接口中获取到一双鞋子的数据 包括pass """
            product = shoe['product']
            shoeStyle = product['style']
            if shoeStyle == '999999':
                shoeDict = {
                    'id': n,
                    'shoeName': shoe['name'],
                    'shoeImageUrl': shoe['imageUrl'],
                    'shoeColor': '',
                    'shoeStyleCode': '',
                    'shoeSelectMethod': '',
                    'shoePrice': '',
                    'shoeSize': '',
                    'shoePublishTime': ''
                }
            else:
                shoeSize = ''
                for sku in product['skus']:
                    shoeSize = '{}|{}'.format(shoeSize, sku['localizedSize'])
                try:
                    selector = product['selectionEngine']
                except KeyError:
                    selector = None
                shoeDict = {
                    'id': n,
                    'shoeName': shoe['name'],
                    'shoeColor': product['colorDescription'],
                    'shoeImageUrl': product['imageUrl'],
                    'shoeStyleCode': "{}-{}".format(product['style'], product['colorCode']),
                    'shoeSelectMethod': selector,
                    'shoePrice': product['price']['msrp'],
                    'shoeSize': shoeSize,
                    'shoePublishTime': product['startSellDate'][:20].replace('T', ' ')
                    }
            n += 1
            shoesData.append(shoeDict)
        return shoesData


if __name__ == '__main__':
    shoesdata = AppSpiders().spiderDate()
    db = db()
    db.dropTable(table='shoes')
    db.init()
    insertData = []
    for d in shoesdata:
        insertdata = (
            d['id'],
            d['shoeName'],
            d['shoeColor'],
            d['shoeImageUrl'],
            d['shoeStyleCode'],
            d['shoeSelectMethod'],
            d['shoePrice'],
            d['shoeSize'],
            d['shoePublishTime']
            )
        insertData.append(insertdata)
    insertSql = """INSERT INTO shoes VALUES (?,?,?,?,?,?,?,?,?) """
    db.insertData(sql=insertSql, d=insertData)
    fetchSql = """SELECT * FROM shoes limit 10"""
    values = db.fetchData(sql=fetchSql, c=None)
    print(values)
