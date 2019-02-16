#!/usr/bin/env python
# coding=utf-8

from async_proxy_pool.webapi_flask import app
from async_proxy_pool.config import SERVER_HOST, SERVER_PORT, SERVER_ACCESS_LOG

# 启动服务端 Flask app
app.run(host=SERVER_HOST, port=SERVER_PORT, debug=SERVER_ACCESS_LOG)
