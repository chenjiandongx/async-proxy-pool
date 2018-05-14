#!/usr/bin/env python
# coding=utf-8

import aiohttp
import asyncio

from async_proxy_pool.config import TEST_BASE_URL, TEST_BATCH_COUNT
from async_proxy_pool.logger import logger
from async_proxy_pool.database import RedisClient


class Validator:

    def __init__(self):
        self.redis = RedisClient()

    async def test_proxy(self, proxy: str) -> None:
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode("utf8")
                async with session.get(
                    TEST_BASE_URL, proxy=proxy, timeout=10
                ) as resp:
                    if resp.status == 200:
                        logger.info("Validator √ {}".format(proxy))
                    else:
                        logger.info("Validator x {}".format(proxy))
                        self.redis.decrease(proxy)
            except:
                self.redis.decrease(proxy)
                logger.info("Validator x {}".format(proxy))

    def run(self) -> None:
        logger.info("Validator working...")
        proxies = self.redis.all()
        loop = asyncio.get_event_loop()
        for i in range(0, len(proxies), TEST_BATCH_COUNT):
            _proxies = proxies[i:i + TEST_BATCH_COUNT]
            tasks = [self.test_proxy(proxy) for proxy in _proxies]
            if tasks:
                loop.run_until_complete(asyncio.wait(tasks))


validator = Validator()
