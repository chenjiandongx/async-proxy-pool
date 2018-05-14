#!/usr/bin/env python
# coding=utf-8

TEST_BASE_URL = "https://httpbin.org/"
TEST_BATCH_COUNT = 100

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_KEY = "proxies"

MAX_SCORE = 10
MIN_SCORE = 0

VALIDATOR_RUN_CYCLE = 30
CRAWLER_RUN_CYCLE = 30

HEADERS = {
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
}
