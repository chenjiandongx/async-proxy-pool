#!/usr/bin/env python
# coding=utf-8

import asyncio

import aiohttp

from .config import HEADERS


async def _get_page(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS) as resp:
            return await resp.text()


def requests(url: str) -> str:
    loop = asyncio.get_event_loop()
    html = loop.run_until_complete(asyncio.gather(_get_page(url)))
    return "".join(html)
