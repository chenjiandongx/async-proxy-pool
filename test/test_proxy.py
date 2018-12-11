#!/usr/bin/env python
# coding=utf-8

import os
import random
from concurrent.futures import ThreadPoolExecutor

import requests


HEADERS = {
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
}

SUCCESS = 0
FAIL = 0
TIMEOUT = 15

TEST_COUNT = os.environ.get("TEST_COUNT") or 1000
TEST_WEBSITE = os.environ.get("TEST_WEBSITE") or "https://zhihu.com"
TEST_PROXIES = os.environ.get("TEST_PROXIES") or "http://localhost:3289/get/20"


def get_proxies():
    _proxies = requests.get(TEST_PROXIES, timeout=TIMEOUT).json()
    for proxy in _proxies:
        if "http" in proxy.keys():
            proxy["https"] = proxy["http"]
    return _proxies


def test_one_proxy(proxy):
    global SUCCESS, FAIL
    try:
        req = requests.get(
            TEST_WEBSITE, proxies=proxy, timeout=TIMEOUT, headers=HEADERS
        )
        if req.status_code == 200:
            SUCCESS += 1
        else:
            FAIL += 1
    except:
        FAIL += 1


if __name__ == "__main__":
    proxies = get_proxies()
    tasks = [random.choice(proxies) for _ in range(int(TEST_COUNT))]
    with ThreadPoolExecutor(max_workers=64) as executor:
        executor.map(test_one_proxy, tasks)
    print("测试代理：", TEST_PROXIES)
    print("测试网站：", TEST_WEBSITE)
    print("测试次数：", TEST_COUNT)
    print("成功次数：", SUCCESS)
    print("失败次数：", FAIL)
    print("成功率：", SUCCESS / TEST_COUNT)
