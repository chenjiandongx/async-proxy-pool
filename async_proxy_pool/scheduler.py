#!/usr/bin/env python
# coding=utf-8

import time

import schedule

from .config import CRAWLER_RUN_CYCLE, VALIDATOR_RUN_CYCLE

from .crawler import crawler
from .validator import validator
from .logger import logger


def run_schedule():
    """
    启动客户端
    """
    # 启动收集器
    schedule.every(CRAWLER_RUN_CYCLE).minutes.do(crawler.run).run()
    # 启动验证器
    schedule.every(VALIDATOR_RUN_CYCLE).minutes.do(validator.run).run()

    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            logger.info("You have canceled all jobs")
            return
