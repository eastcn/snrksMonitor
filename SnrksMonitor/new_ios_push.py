"""
author:hefeng
function:push message to ios users with the help of BARK
"""
import requests
import yaml
from SnrksMonitor.log import Logger

log = Logger().log()


class PushToIos:
    def __init__(self):
        self.push_url = "https://api.day.app/"
        self.push_list = [
            {
                "key": '123',
                "name": "east"
            }
        ]

    def push(self, message):
        for member in self.push_list:
            msg = f"{self.push_url}{member['key']}/{message}"
            requests.get(msg)
            log.info(f"推送成功--{member['name']}/{msg}")

