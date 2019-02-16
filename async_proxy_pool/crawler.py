#!/usr/bin/env python
# coding=utf-8

import re

import pyquery

from .utils import requests
from .database import RedisClient
from .logger import logger


redis_conn = RedisClient()
all_funcs = []


def collect_funcs(func):
    """
    装饰器，用于收集爬虫函数
    """
    all_funcs.append(func)
    return func


class Crawler:
    @staticmethod
    def run():
        """
        启动收集器
        """
        logger.info("Crawler working...")
        for func in all_funcs:
            for proxy in func():
                redis_conn.add_proxy(proxy)
                logger.info("Crawler √ {}".format(proxy))
        logger.info("Crawler resting...")

    @staticmethod
    @collect_funcs
    def crawl_66ip():
        """
        66ip 代理：http://www.66ip.cn
        """
        url = (
            "http://www.66ip.cn/nmtq.php?getnum=100&isp=0"
            "&anonymoustype=0&area=0&proxytype={}&api=66ip"
        )
        pattern = "\d+\.\d+.\d+\.\d+:\d+"

        items = [(0, "http://{}"), (1, "https://{}")]
        for item in items:
            proxy_type, host = item
            html = requests(url.format(proxy_type))
            if html:
                for proxy in re.findall(pattern, html):
                    yield host.format(proxy)

    @staticmethod
    @collect_funcs
    def crawl_xici():
        """
        西刺代理：http://www.xicidaili.com
        """
        url = "http://www.xicidaili.com/{}"

        items = []
        for page in range(1, 21):
            items.append(("wt/{}".format(page), "http://{}:{}"))
            items.append(("wn/{}".format(page), "https://{}:{}"))

        for item in items:
            proxy_type, host = item
            html = requests(url.format(proxy_type))
            if html:
                doc = pyquery.PyQuery(html)
                for proxy in doc("table tr").items():
                    ip = proxy("td:nth-child(2)").text()
                    port = proxy("td:nth-child(3)").text()
                    if ip and port:
                        yield host.format(ip, port)

    @staticmethod
    @collect_funcs
    def crawl_kuaidaili():
        """
        快代理：https://www.kuaidaili.com
        """
        url = "https://www.kuaidaili.com/free/{}"

        items = ["inha/1/"]
        for proxy_type in items:
            html = requests(url.format(proxy_type))
            if html:
                doc = pyquery.PyQuery(html)
                for proxy in doc(".table-bordered tr").items():
                    ip = proxy("[data-title=IP]").text()
                    port = proxy("[data-title=PORT]").text()
                    if ip and port:
                        yield "http://{}:{}".format(ip, port)

    @staticmethod
    @collect_funcs
    def crawl_ip3366():
        """
        云代理：http://www.ip3366.net
        """
        url = "http://www.ip3366.net/?stype=1&page={}"

        items = [p for p in range(1, 8)]
        for page in items:
            html = requests(url.format(page))
            if html:
                doc = pyquery.PyQuery(html)
                for proxy in doc(".table-bordered tr").items():
                    ip = proxy("td:nth-child(1)").text()
                    port = proxy("td:nth-child(2)").text()
                    schema = proxy("td:nth-child(4)").text()
                    if ip and port and schema:
                        yield "{}://{}:{}".format(schema.lower(), ip, port)

    @staticmethod
    @collect_funcs
    def crawl_data5u():
        """
        无忧代理：http://www.data5u.com/
        """
        url = "http://www.data5u.com/"

        html = requests(url)
        if html:
            doc = pyquery.PyQuery(html)
            for index, item in enumerate(doc("li ul").items()):
                if index > 0:
                    ip = item("span:nth-child(1)").text()
                    port = item("span:nth-child(2)").text()
                    schema = item("span:nth-child(4)").text()
                    if ip and port and schema:
                        yield "{}://{}:{}".format(schema, ip, port)

    @staticmethod
    @collect_funcs
    def crawl_iphai():
        """
        ip 海代理：http://www.iphai.com
        """
        url = "http://www.iphai.com/free/{}"

        items = ["ng", "np", "wg", "wp"]
        for proxy_type in items:
            html = requests(url.format(proxy_type))
            if html:
                doc = pyquery.PyQuery(html)
                for item in doc(".table-bordered tr").items():
                    ip = item("td:nth-child(1)").text()
                    port = item("td:nth-child(2)").text()
                    schema = item("td:nth-child(4)").text().split(",")[0]
                    if ip and port and schema:
                        yield "{}://{}:{}".format(schema.lower(), ip, port)

    @staticmethod
    @collect_funcs
    def crawl_swei360():
        """
        360 代理：http://www.swei360.com
        """
        url = "http://www.swei360.com/free/?stype={}"

        items = [p for p in range(1, 5)]
        for proxy_type in items:
            html = requests(url.format(proxy_type))
            if html:
                doc = pyquery.PyQuery(html)
                for item in doc(".table-bordered tr").items():
                    ip = item("td:nth-child(1)").text()
                    port = item("td:nth-child(2)").text()
                    schema = item("td:nth-child(4)").text()
                    if ip and port and schema:
                        yield "{}://{}:{}".format(schema.lower(), ip, port)


crawler = Crawler()
