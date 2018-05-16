#!/usr/bin/env python
# coding=utf-8

import aiohttp
import asyncio

from .config import TEST_BASE_URL, TEST_BATCH_COUNT, REQUEST_TIMEOUT
from .logger import logger
from .database import RedisClient


class Validator:

    def __init__(self):
        self.redis = RedisClient()

    async def test_proxy(self, proxy):
        """
        测试代理

        :param proxy: 指定代理
        """
        async with aiohttp.ClientSession() as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode("utf8")
                async with session.get(
                    TEST_BASE_URL, proxy=proxy, timeout=REQUEST_TIMEOUT
                ) as resp:
                    if resp.status == 200:
                        logger.info("Validator √ {}".format(proxy))
                    else:
                        logger.info("Validator × {}".format(proxy))
                        self.redis.reduce_proxy_score(proxy)
            except:
                self.redis.reduce_proxy_score(proxy)
                logger.info("Validator × {}".format(proxy))

    def run(self):
        """
        启动校验器
        """
        logger.info("Validator working...")
        proxies = self.redis.all_proxies()
        loop = asyncio.get_event_loop()
        for i in range(0, len(proxies), TEST_BATCH_COUNT):
            _proxies = proxies[i:i + TEST_BATCH_COUNT]
            tasks = [self.test_proxy(proxy) for proxy in _proxies]
            if tasks:
                loop.run_until_complete(asyncio.wait(tasks))


validator = Validator()
