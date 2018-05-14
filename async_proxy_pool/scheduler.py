#!/usr/bin/env python
# coding=utf-8

import time

import schedule

from async_proxy_pool.config import CRAWLER_RUN_CYCLE, VALIDATOR_RUN_CYCLE

from async_proxy_pool.crawler import crawler
from async_proxy_pool.validator import validator

schedule.every(CRAWLER_RUN_CYCLE).minutes.do(crawler.run).run()
schedule.every(VALIDATOR_RUN_CYCLE).minutes.do(validator.run).run()

while True:
    schedule.run_pending()
    time.sleep(1)
