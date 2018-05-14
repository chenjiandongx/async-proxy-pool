#!/usr/bin/env python
# coding=utf-8

import re
from types import FunctionType

from .utils import requests
from .database import RedisClient
from .logger import logger


all_funcs = []


def collect_funcs(func: FunctionType) -> FunctionType:
    all_funcs.append(func)
    return func


class Crawler:

    @staticmethod
    def run() -> None:
        redis = RedisClient()
        logger.info("Crawler working...")
        for func in all_funcs:
            for proxy in func():
                logger.info("Crawler √ {}".format(proxy))
                redis.add(proxy)

    @staticmethod
    @collect_funcs
    def crawl_66ip() -> list:
        url = (
            "http://www.66ip.cn/nmtq.php?getnum=100&isp=0"
            "&anonymoustype=0&area=0&proxytype={}&api=66ip"
        )
        pattern = "\d+\.\d+.\d+\.\d+:\d+"

        def get_urls(proxy_type, host):
            html = requests(url.format(proxy_type))
            urls = [host.format(u) for u in re.findall(pattern, html)]
            return urls

        items, res = [(0, "http://{}"), (1, "https://{}")], []
        for item in items:
            res.extend(get_urls(*item))
        return res


crawler = Crawler()
