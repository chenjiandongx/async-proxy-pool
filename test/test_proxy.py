#!/usr/bin/env python
# coding=utf-8


import random
import asyncio

import requests
import aiohttp


SUCCESS = 0
FAIL = 0
TEST_COUNT = 1000
TEST_WEBSITE = "https://httpbin.org/"
PROXIES_URL = "http://localhost:3289/get/20"


async def test_proxy(proxy, url):
    global SUCCESS, FAIL
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, proxy=proxy, timeout=15) as resp:
                if resp.status == 200:
                    SUCCESS += 1
                else:
                    FAIL += 1
        except:
            FAIL += 1


def get_proxies(proxies_url):
    proxies = requests.get(proxies_url).json()
    _proxies = []
    for proxy in proxies:
        for p in proxy.values():
            _proxies.append(p)
    return _proxies


if __name__ == "__main__":
    proxies = get_proxies(PROXIES_URL)
    loop = asyncio.get_event_loop()
    tasks = [
        test_proxy(random.choice(proxies), TEST_WEBSITE)
        for _ in range(TEST_COUNT)
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    print("测试网站：", TEST_WEBSITE)
    print("成功次数：", SUCCESS)
    print("失败次数：", FAIL)
    print("成功率：", SUCCESS / TEST_COUNT)
