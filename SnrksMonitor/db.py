"""
create to db
"""
import sqlite3
import yaml
from SnrksMonitor.log import Logger

log = Logger().log()

class db:
    def __init__(self):
        file = './config.yaml'
        try:
            f = open(file, 'r', encoding='UTF-8')
            global configdata
            configdata = yaml.load(f)
        except IOError:
            # logging.log('open config failed')
            log.info('open config failed')

        self.databasePath = configdata['db']['db_path']
        self.table_name = configdata['db']['table_name']

    def getConn(self, path):
        """
        获取数据库连接
        :return: 返回数据库连接对象
        """
        if path is not None:
            conn = sqlite3.connect(path)
            return conn
        else:
            conn = sqlite3.connect(self.databasePath)
            return conn

    def getCursor(self, conn):
        """
        获取数据库连接游标
        :return: 返回数据库连接游标
        """
        if conn is not None:
            return conn.cursor()
        else:
            return self.getConn(path=None).cursor()

    def createTable(self, c, sql):
        """
        创建数据库
        :return:
        """
        if sql is not None and sql != '':
            conn = self.getConn(c)
            cu = self.getCursor(conn)
            cu.execute(sql)
            conn.commit()
            log.info('数据库创建成功')
            cu.close()
            conn.close()
        else:
            log.info('sql不正确')

    def dropTable(self, table):
        """
        删表,暂时用不上，所以pass
        :return:
        """
        conn = self.getConn(None)
        cu = self.getCursor(conn)
        dropSql = """DROP TABLE '{}' """.format(table)
        cu.execute(dropSql)
        conn.commit()
        log.info('数据库表{}删除成功'.format(table))
        cu.close()
        conn.close()

    def insertData(self, sql, d):
        """
        插入数据
        :param sql: 插入的sql语句
        :param d: 插入的数据
        :return:
        """
        if sql is not None and sql != ' ':
            if d is not None:
                conn = self.getConn(None)
                cu = self.getCursor(conn)
                for data in d:
                    cu.execute(sql, data)
                    conn.commit()
                cu.close()
                conn.close()
                log.info('数据库数据插入成功')
            else:
                log.info('没有数据')
        else:
            log.info('没有sql')

    def fetchData(self, sql, c):
        """
        查询数据
        :param sql:
        :return:
        """
        if sql is not None and sql != ' ':
            conn = self.getConn(c)
            cu = self.getCursor(conn)
            value = cu.execute(sql).fetchall()
            cu.close()
            conn.close()
            return value
        else:
            log.info('sql为空')
            return 'failed'

    def deleteData(self, sql):
        """
        删除数据
        :param c:
        :param sql:
        :param d:
        :return:
        """
        if sql is not None and sql != ' ':
            conn = self.getConn(None)
            cu = self.getCursor(conn)
            cu.execute(sql)
            conn.commit()
            cu.close()
            conn.close()
            log.info('数据库中数据删除成功')
        else:
            log.info('sql为空')

    def init_shoes(self):
        createTableSql = """CREATE TABLE 'shoes'(
                            'id' INTEGER PRIMARY KEY AUTOINCREMENT,
                            'shoename' varchar (30),
		                    'shoeColor' varchar (30), 
		                    'shoeImageUrl' varchar (100),
		                    'shoeImage' varchar(100),
		                    'shoeStyleCode' varchar (50), 
		                    'shoeSelectMethod' varchar (20),
                            'shoePrice' varchar (10),
                            'shoeSize' varchar (100),
                            'shoePublishTime' varchar (100),
                            'shoeCountry' varchar(10)
                            )"""
        self.createTable(c=None, sql=createTableSql)


    def updateShoesTable(self, data):
        """
        对鞋子表进行更新
        :param data:
        :return:
        """
        # 删除鞋子表中的数据
        # deleteShoesSql = """DELETE FROM shoes where id < 1000"""
        # log.info('鞋子的久数据删除中')
        # self.deleteData(sql=deleteShoesSql)
        # log.info('鞋子的久数据删除完成')
        # 把最新的数据插入鞋子库
        log.info('更新的鞋子数据插入中')
        insertSql = """INSERT INTO shoes values (?,?,?,?,?,?,?,?,?,?,?)"""
        insertData = []
        # 把传进来的字典数据 转成插入数据库的数据tulble
        for item in data:
            dataturple = (
                item['id'],
                item ['shoeName'],
                item ['shoeColor'],
                item ['shoeImageUrl'],
                item ['shoeImage'],
                item ['shoeStyleCode'],
                item ['shoeSelectMethod'],
                item ['shoePrice'],
                item ['shoeSize'],
                item ['shoePublishTime'],
                item ['shoeCountry']
            )
            insertData.append (dataturple)
        self.insertData (sql=insertSql, d=insertData)
        log.info('鞋子的最新数据插入成功')

if __name__ == '__main__':
    db = db()
    db.dropTable(table='shoes')
    db.dropTable(table='update')
    db.init_shoes()
    createTableSql = """CREATE TABLE 'update'(
                                'id' INTEGER PRIMARY KEY AUTOINCREMENT,
                                'shoename' varchar (30),
    		                    'shoeColor' varchar (30), 
    		                    'shoeImageUrl' varchar (100),
    		                    'shoeImage' varchar(100),
    		                    'shoeStyleCode' varchar (50), 
    		                    'shoeSelectMethod' varchar (20),
                                'shoePrice' varchar (10),
                                'shoeSize' varchar (100),
                                'shoePublishTime' varchar (100),
                                'shoeCountry' varchar(10)
                                )"""
    db.createTable(c=None, sql= createTableSql)
    # db.init()
    # insertSql = """INSERT INTO shoes values (?,?,?,?,?,?,?,?,?)"""
    # insertData = [
    #     (
    #         1, 'shoeName', '1asd/asd/asd', 'https://23123123', 'abc-123123',
    #         'leo',
    #         '1299',
    #         '1,2,3,4,5,6,7',
    #         '2019-2-19 9:00'
    #     )
    # ]
    # db.insertData(sql=insertSql, d=insertData)
    #
    # fetchSql = """SELECT * FROM shoes"""
    # data = db.fetchData(sql=fetchSql, c=None)
    # log.info(data)
