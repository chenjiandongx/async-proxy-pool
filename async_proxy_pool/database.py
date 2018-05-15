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
        if not self.redis.zscore(REDIS_KEY, proxy):
            self.redis.zadd(REDIS_KEY, proxy, score)

    def decrease(self, proxy):
        score = self.redis.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            self.redis.zincrby(REDIS_KEY, proxy, -1)
        else:
            self.redis.zrem(REDIS_KEY, proxy)

    def pop(self):
        result = self.redis.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if result:
            return random.choice(result)
        else:
            result = self.redis.zrevrange(REDIS_KEY, MIN_SCORE, MAX_SCORE)
            if result:
                return random.choice(result)

    def get(self, count=1):
        result = self.redis.zrevrange(REDIS_KEY, MIN_SCORE, MAX_SCORE)
        for index, value in enumerate(result):
            if index < count:
                yield value.decode("utf-8")

    def count(self):
        return self.redis.zcard(REDIS_KEY)

    def all(self):
        return self.redis.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)


redis_conn = RedisClient()
