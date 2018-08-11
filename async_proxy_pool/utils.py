#!/usr/bin/env python
# coding=utf-8

import asyncio

import aiohttp

from .config import HEADERS, REQUEST_TIMEOUT, REQUEST_DELAY


LOOP = asyncio.get_event_loop()


async def _get_page(url, sleep):
    """
    获取并返回网页内容
    """
    async with aiohttp.ClientSession() as session:
        try:
            await asyncio.sleep(sleep)
            async with session.get(
                url, headers=HEADERS, timeout=REQUEST_TIMEOUT
            ) as resp:
                return await resp.text()
        except:
            return ""


def requests(url, sleep=REQUEST_DELAY):
    """
    请求方法，用于获取网页内容

    :param url: 请求链接
    :param sleep: 延迟时间（秒）
    """
    html = LOOP.run_until_complete(asyncio.gather(_get_page(url, sleep)))
    if html:
        return "".join(html)
