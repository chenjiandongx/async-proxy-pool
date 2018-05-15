#!/usr/bin/env python
# coding=utf-8

import random

import redis

from .config import (
    REDIS_KEY,
    REDIS_PORT,
    REDIS_PASSWORD,
    REDIS_HOST,
    MAX_SCORE,
    MIN_SCORE,
)


class RedisClient:

    def __init__(
        self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD
    ):
        self.redis = redis.Redis(host=host, port=port, password=password)

    def add(self, proxy, score=MAX_SCORE):
        """
        新增一个代理

        :param proxy: 新增代理
        :param score: 初始化分数
        """
        if not self.redis.zscore(REDIS_KEY, proxy):
            self.redis.zadd(REDIS_KEY, proxy, score)

    def decrease(self, proxy):
        """
        验证为通过，分数减一

        :param proxy: 验证代理
        """
        score = self.redis.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            self.redis.zincrby(REDIS_KEY, proxy, -1)
        else:
            self.redis.zrem(REDIS_KEY, proxy)

    def pop(self):
        """
        返回一个代理
        """
        result = self.redis.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if result:
            return random.choice(result)
        else:
            result = self.redis.zrevrange(REDIS_KEY, MIN_SCORE, MAX_SCORE)
            if result:
                return random.choice(result)

    def get(self, count=1):
        """
        返回指定数量代理，分数由高到低排序

        :param count: 代理数量
        """
        result = self.redis.zrevrange(REDIS_KEY, MIN_SCORE, MAX_SCORE)
        for index, value in enumerate(result):
            if index < count:
                yield value.decode("utf-8")

    def count(self):
        """
        返回代理总数
        """
        return self.redis.zcard(REDIS_KEY)

    def all(self):
        """
        返回全部代理
        """
        return self.redis.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)


redis_conn = RedisClient()
