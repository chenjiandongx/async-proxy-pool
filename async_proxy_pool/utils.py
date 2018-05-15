#!/usr/bin/env python
# coding=utf-8

import asyncio

import aiohttp

from .config import HEADERS, REQUEST_TIMEOUT


async def _get_page(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
                url, headers=HEADERS, timeout=REQUEST_TIMEOUT
            ) as resp:
                return await resp.text()
        except:
            return ""


def requests(url):
    loop = asyncio.get_event_loop()
    html = loop.run_until_complete(asyncio.gather(_get_page(url)))
    if html:
        return "".join(html)
