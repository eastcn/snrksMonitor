"""
工具类
"""
import yaml
import traceback

config_url = '../config.yaml'


class utils:
	def __init__(self):
		pass

	def readconfig(self):
		"""
		读取配置
		:return:配置字典
		"""
		try:
			f = open(config_url, 'r', encoding='UTF-8')
			global configdata
			configdict = yaml.load(f)
		except IOError as e:
			# logging.log('open config failed')
			configdict = {}
			print('open config failed\n {}'.format(traceback.format_exc()))
		return configdict
