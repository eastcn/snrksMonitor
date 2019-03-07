"""
create to db
"""
import sqlite3
import yaml
from SnrksMonitor import log


class db:
	def __init__(self):
		file = './config.yaml'
		try:
			f = open (file, 'r', encoding='UTF-8')
			global configdata
			configdata = yaml.load (f)
		except IOError:
			# logging.log('open config failed')
			print ('open config failed')

		self.databasePath = configdata['db']['db_path']
		self.table_name = configdata['db']['table_name']

	def getConn(self,path):
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


	def getCursor(self,conn):
		"""
		获取数据库连接游标
		:return: 返回数据库连接游标
		"""
		if conn is not None:
			return conn.cursor()
		else:
			return self.getConn(path=None).cursor()


	def createTable(self,c,sql):
		"""
		创建数据库
		:return:
		"""
		if sql is not None and sql != '':
			conn = self.getConn(c)
			cu = self.getCursor(conn)
			cu.execute(sql)
			conn.commit()
			print('数据库创建成功')
			cu.close()
			conn.close()
		else:
			print('sql不正确')


	def dropTable(self):
		"""
		删表,暂时用不上，所以pass
		:return:
		"""
		pass

	def insertData(self,sql,d):
		"""
		插入数据
		:param sql: 插入的sql语句
		:param data: 插入的数据
		:return:
		"""
		if sql is not None and sql != ' ':
			if d is not None:
				conn = self.getConn(None)
				cu = self.getCursor(conn)
				for data in d:
					cu.execute(sql,data)
					conn.commit()
				cu.close()
				conn.close()
				print('插入成功')
			else:
				print('没有数据')
		else:
			print('没有sql')


	def fetchData(self,sql,c):
		"""
		查询数据
		:param sql:
		:return:
		"""
		if sql is not None and sql != ' ':
			conn =self.getConn(c)
			cu = self.getCursor(conn)
			value = cu.execute(sql).fetchall()
			cu.close()
			conn.close()
			return value
		else:
			print('sql为空')
			return 'failed'


	def deleteData(self,c,sql,d):
		"""
		删除数据
		:param c:
		:param sql:
		:param d:
		:return:
		"""
		if sql is not None and sql != ' ':
			conn =self.getConn(c)
			cu = self.getConn(conn)
			for data in d:
				cu.execute(sql)
				conn.commit()
			cu.close()
			conn.close()
		else:
			print('sql为空')


	def init(self):
		createTableSql = """CREATE TABLE 'shoe'(
		'id' int(10) NOT NULL PRIMARY KEY,
		'shoename' varchar (30),
		'shoeColor' varchar (30),
		'shoeImageUrl' varchar (100),
		'shoeStyleCode' varchar (50),
		'shoeSelectMethod' varchar (20),
		'shoePrice' varchar (10),
		'shoeSize' varchar (100),
		'shoePublishTime' varchar (100)
		)"""
		self.createTable(c=None,sql=createTableSql)


if __name__ == '__main__':
	db = db()
	insertSql = """
	INSERT INTO shoes values (?,?,?,?,?,?,?,?,?)
	"""
	insertData = [
		(
		1,'shoeName','1asd/asd/asd', 'https://23123123', 'abc-123123',
		 'leo',
		 '1299',
		'1,2,3,4,5,6,7',
		 '2019-2-19 9:00'
		)
	]
	db.insertData(sql=insertSql,d=insertData)

	fetchSql = """SELECT * FROM shoes
	"""
	data = db.fetchData(sql=fetchSql,c=None)
	print(data)


