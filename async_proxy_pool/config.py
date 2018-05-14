#!/usr/bin/env python
# coding=utf-8

# 校验器测试网站
TEST_BASE_URL = "https://httpbin.org/"
# 批量测试数量
TEST_BATCH_COUNT = 100

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_KEY = "proxies"

# REDIS SCORE 最大分数
MAX_SCORE = 10
# REDIS SCORE 最小分数
MIN_SCORE = 0

# sanic web host
SANIC_HOST = "localhost"
# sanic web port
SANIC_PORT = 3289

# 校验器循环周期（分钟）
VALIDATOR_RUN_CYCLE = 15
# 爬取器循环周期（分钟）
CRAWLER_RUN_CYCLE = 30

HEADERS = {
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
}
