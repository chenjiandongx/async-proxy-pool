#!/usr/bin/env python
# coding=utf-8

from async_proxy_pool.webapi import app
from async_proxy_pool.config import SANIC_HOST, SANIC_PORT


# 启动服务端 app
# 取消日志记录可以提高服务器性能
app.run(host=SANIC_HOST, port=SANIC_PORT, access_log=False)
