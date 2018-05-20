#!/usr/bin/env python
# coding=utf-8

import os
import random
import asyncio

import aiohttp


SUCCESS = 0
FAIL = 0
TIMEOUT = 15

TEST_COUNT = int(os.environ.get("TEST_COUNT")) or 1000
TEST_WEBSITE = os.environ.get("TEST_WEBSITE") or "https://httpbin.org/"
TEST_PROXIES = os.environ.get("TEST_PROXIES") or "http://localhost:3289/get/20"


async def test_proxy(proxy, url):
    global SUCCESS, FAIL
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, proxy=proxy, timeout=TIMEOUT) as resp:
                if resp.status == 200:
                    SUCCESS += 1
                else:
                    FAIL += 1
        except:
            FAIL += 1


async def get_proxies():
    async with aiohttp.ClientSession() as sess:
        async with sess.get(TEST_PROXIES, timeout=TIMEOUT) as resp:
            _proxies = []
            for proxy in await resp.json():
                for p in proxy.values():
                    _proxies.append(p)
            return _proxies


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    proxies = loop.run_until_complete(get_proxies())
    tasks = [
        test_proxy(random.choice(proxies), TEST_WEBSITE)
        for _ in range(TEST_COUNT)
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    print("测试网站：", TEST_WEBSITE)
    print("成功次数：", SUCCESS)
    print("失败次数：", FAIL)
    print("成功率：", SUCCESS / TEST_COUNT)
