#!/usr/bin/env python
# coding=utf-8

import random

import redis

from async_proxy_pool.config import (
    REDIS_KEY,
    REDIS_PORT,
    REDIS_PASSWORD,
    REDIS_HOST,
    MAX_SCORE,
    MIN_SCORE,
)


class RedisClient:

    def __init__(
        self,
        host: str = REDIS_HOST,
        port: int = REDIS_PORT,
        password: str = REDIS_PASSWORD,
    ):
        self.redis = redis.Redis(host=host, port=port, password=password)

    def add(self, proxy: str, score: int = MAX_SCORE) -> None:
        if not self.redis.zscore(REDIS_KEY, proxy):
            self.redis.zadd(REDIS_KEY, proxy, score)

    def decrease(self, proxy: str) -> None:
        score = self.redis.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            self.redis.zincrby(REDIS_KEY, proxy, -1)
        else:
            self.redis.zrem(REDIS_KEY, proxy)

    def pop(self) -> str:
        result = self.redis.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if result:
            return random.choice(result)
        else:
            result = self.redis.zrevrange(REDIS_KEY, MIN_SCORE, MAX_SCORE)
            if result:
                return random.choice(result)

    def count(self) -> int:
        return self.redis.zcard(REDIS_KEY)

    def all(self) -> list:
        return self.redis.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)
