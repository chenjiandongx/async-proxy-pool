#!/usr/bin/env python
# coding=utf-8

import time

import schedule

from .config import CRAWLER_RUN_CYCLE, VALIDATOR_RUN_CYCLE

from .crawler import crawler
from .validator import validator


def run_schedule():
    schedule.every(CRAWLER_RUN_CYCLE).minutes.do(crawler.run).run()
    schedule.every(VALIDATOR_RUN_CYCLE).minutes.do(validator.run).run()

    while True:
        schedule.run_pending()
        time.sleep(1)
