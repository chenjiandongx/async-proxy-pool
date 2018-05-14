#!/usr/bin/env python
# coding=utf-8

from sanic import Sanic
from sanic.response import json

from async_proxy_pool.database import redis_conn

app = Sanic()


@app.route("/")
async def test(request):
    return json({"Welcome": "This is a proxy pool system."})


@app.route("/pop")
async def pop_proxy(request):
    proxy = redis_conn.pop().decode("utf8")
    if proxy[:5] == "https":
        return json({"https": proxy})
    else:
        return json({"http": proxy})


@app.route("/count")
async def count_proxies(request):
    count = redis_conn.count()
    return json({"count": str(count)})
