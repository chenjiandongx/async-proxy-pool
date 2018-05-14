#!/usr/bin/env python
# coding=utf-8

import re
from types import FunctionType

import pyquery

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
        """
        启动收集器
        """
        redis = RedisClient()
        logger.info("Crawler working...")
        for func in all_funcs:
            for proxy in func():
                logger.info("Crawler √ {}".format(proxy))
                redis.add(proxy)

    @staticmethod
    @collect_funcs
    def crawl_66ip() -> list:
        """
        66ip 代理：http://www.66ip.cn
        """
        url = (
            "http://www.66ip.cn/nmtq.php?getnum=100&isp=0"
            "&anonymoustype=0&area=0&proxytype={}&api=66ip"
        )
        pattern = "\d+\.\d+.\d+\.\d+:\d+"

        def get_proxies(proxy_type, host):
            html = requests(url.format(proxy_type))
            if html:
                for proxy in re.findall(pattern, html):
                    yield host.format(proxy)

        items, res = [(0, "http://{}"), (1, "https://{}")], []
        for item in items:
            res.extend(get_proxies(*item))
        return res

    @staticmethod
    @collect_funcs
    def crawl_xici() -> list:
        """
        西刺代理：http://www.xicidaili.com
        """
        url = "http://www.xicidaili.com/{}"

        def get_proxies(proxy_type, host):
            html = requests(url.format(proxy_type))
            if html:
                doc = pyquery.PyQuery(html)
                for proxy in doc("table tr").items():
                    ip = proxy("td:nth-child(2)").text()
                    port = proxy("td:nth-child(3)").text()
                    if ip and port:
                        yield host.format(ip, port)

        res, items = [], []
        for page in range(1, 11):
            items.append(("wt/{}".format(page), "http://{}:{}"))
            items.append(("wn/{}".format(page), "https://{}:{}"))
        for item in items:
            res.extend(get_proxies(*item))
        return res


crawler = Crawler()
