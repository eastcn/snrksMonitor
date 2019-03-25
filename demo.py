import requests
import json
import sqlite3

def check_start_selldate():
    url = 'https://api.nike.com/snkrs/content/v1/?country=JP&language=ja&offset=0&orderBy=published'
    r = json.loads(requests.get(url).text)
    for item in r["threads"]:
        try:
            print('{},{}'.format(item['name'],item['product']['startSellDate']))
        except:
            print(item["product"]["style"])


def dbRead():
    db = sqlite3.connect('./SnrksDataBase.db')
    cusor = db.cursor()
    sql = """select shoeStyleCode, shoePublishTime from shoes"""
    datas = cusor.execute(sql)
    return datas


def checl(news):
    datas = dbRead()
    shoeCode = []
    shoePublishTime = []
    for data in datas:
        shoeCode.append(data[0])
        shoePublishTime.append(data[1])
    for new in news:
        pass


if __name__ == "__main__":
    check_start_selldate()