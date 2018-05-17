#!/usr/bin/env python
# coding=utf-8

import random

import redis

from .config import (
    REDIS_KEY,
    REDIS_PORT,
    REDIS_PASSWORD,
    REDIS_HOST,
    REDIS_MAX_CONNECTION,
    MAX_SCORE,
    MIN_SCORE,
)


class RedisClient:

    def __init__(
        self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD
    ):
        conn_pool = redis.ConnectionPool(
            host=host,
            port=port,
            password=password,
            max_connections=REDIS_MAX_CONNECTION,
        )
        self.redis = redis.Redis(connection_pool=conn_pool)

    def add_proxy(self, proxy, score=MAX_SCORE):
        """
        新增一个代理

        :param proxy: 新增代理
        :param score: 初始化分数
        """
        if not self.redis.zscore(REDIS_KEY, proxy):
            self.redis.zadd(REDIS_KEY, proxy, score)

    def reduce_proxy_score(self, proxy):
        """
        验证未通过，分数减一

        :param proxy: 验证代理
        """
        score = self.redis.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            self.redis.zincrby(REDIS_KEY, proxy, -1)
        else:
            self.redis.zrem(REDIS_KEY, proxy)

    def increase_proxy_score(self, proxy):
        """
        验证通过，分数加一

        :param proxy: 验证代理
        """
        score = self.redis.zscore(REDIS_KEY, proxy)
        if score and score < MAX_SCORE:
            self.redis.zincrby(REDIS_KEY, proxy, 1)

    def pop_proxy(self):
        """
        返回一个代理
        """
        # 第一次尝试取分数最高，也就是最新可用的代理
        first_chance = self.redis.zrangebyscore(
            REDIS_KEY, MAX_SCORE, MAX_SCORE
        )
        if first_chance:
            return random.choice(first_chance)

        else:
            # 第二次尝试取 7-10 分数的任意一个代理
            second_chance = self.redis.zrangebyscore(
                REDIS_KEY, MAX_SCORE - 3, MAX_SCORE
            )
            if second_chance:
                return random.choice(second_chance)
            # 最后一次就随便取咯
            else:
                last_chance = self.redis.zrangebyscore(
                    REDIS_KEY, MIN_SCORE, MAX_SCORE
                )
                if last_chance:
                    return random.choice(last_chance)

    def get_proxies(self, count=1):
        """
        返回指定数量代理，分数由高到低排序

        :param count: 代理数量
        """
        result = self.redis.zrevrange(REDIS_KEY, 0, count - 1)
        for r in result:
            yield r.decode("utf-8")

    def count_proxies(self):
        """
        返回代理总数
        """
        return self.redis.zcard(REDIS_KEY)

    def all_proxies(self):
        """
        返回全部代理
        """
        return self.redis.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)


redis_conn = RedisClient()
