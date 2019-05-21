"""
east
"""
import yaml
import logging
import datetime


class Logger:
    """自定义封装logging模块"""

    def __init__(self, default_level=logging.INFO):
        self.logger = logging.getLogger('__name__')
        # 初始化一个logger
        self.default_level = default_level
        logger_main_level, logger_file_level, logger_console_level = self.config()
        self.logger.setLevel(logger_main_level)
        fomatter = logging.Formatter(
            '[%(asctime)s] %(filename)s line:%(lineno)d [%(levelname)s]%(message)s')
        # 初始化输出到日志文件的handle
        file_name = './log/{}log.txt'.format(datetime.datetime.now().strftime('%Y-%m-%d'))
        file_log = logging.FileHandler(filename=file_name, encoding='utf-8')
        file_log.setLevel(logger_file_level)
        file_log.setFormatter(fomatter)
        # 初始化增加输出到控制台的handle
        console_log = logging.StreamHandler()
        console_log.setLevel(logger_console_level)
        console_log.setFormatter(fomatter)

        if self.logger.hasHandlers() is False:
            self.logger.addHandler(file_log)
            self.logger.addHandler(console_log)
        # self.logger.removeHandler(file_log)
        # self.logger.removeHandler(console_log)
        file_log.close()
        console_log.close()

    def config(self):
        """
        :return: 返回配置中读取的level
        """
        try:
            with open('./config.yaml', 'r', encoding='utf-8') as f:
                global config_data
                config_data = yaml.load(f, Loader=yaml.FullLoader)
        except IOError:
            self.logger.error('open config file failed')
        case1 = config_data['logConfig']['testLogLevel']['mainLogLevel']
        case2 = config_data['logConfig']['testLogLevel']['fileLogLevel']
        case3 = config_data['logConfig']['testLogLevel']['consoleLogLevel']
        logger_main_level = self.switch(case=case1)
        logger_file_level = self.switch(case=case2)
        logger_console_level = self.switch(case=case3)
        return logger_main_level, logger_file_level, logger_console_level

    def switch(self, case):
        """
        :param case: 传入需要做判断的level
        :return: 返回最终的level
        """
        if case == 'DEBUG':
            result = logging.DEBUG
        elif case == 'INFO':
            result = logging.DEBUG
        elif case == 'ERROR':
            result = logging.ERROR
        elif case == 'CRITICAL':
            result = logging.CRITICAL
        else:
            result = self.logger.setLevel(self.default_level)
        return result

    def log(self):
        return self.logger
