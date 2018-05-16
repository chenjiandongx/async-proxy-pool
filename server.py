#!/usr/bin/env python
# coding=utf-8

from async_proxy_pool.webapi import app
from async_proxy_pool.config import SANIC_HOST, SANIC_PORT, SANIC_ACCESS_LOG


# 启动服务端 app
app.run(host=SANIC_HOST, port=SANIC_PORT, access_log=SANIC_ACCESS_LOG)
