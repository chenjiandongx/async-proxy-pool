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
    INIT_SCORE,
)


class RedisClient:
    """
    代理池依赖了 Redis 数据库，使用了其`有序集合`的数据结构
    （可按分数排序，key 值不能重复）
    """

    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        conn_pool = redis.ConnectionPool(
            host=host,
            port=port,
            password=password,
            max_connections=REDIS_MAX_CONNECTION,
        )
        self.redis = redis.Redis(connection_pool=conn_pool)

    def add_proxy(self, proxy, score=INIT_SCORE):
        """
        新增一个代理，初始化分数 INIT_SCORE < MAX_SCORE，确保在
        运行完收集器后还没运行校验器就获取代理，导致获取到分数虽为 MAX_SCORE,
        但实际上确是未经验证，不可用的代理

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
        first_chance = self.redis.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
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
                last_chance = self.redis.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)
                if last_chance:
                    return random.choice(last_chance)

    def get_proxies(self, count=1):
        """
        返回指定数量代理，分数由高到低排序

        :param count: 代理数量
        """
        proxies = self.redis.zrevrange(REDIS_KEY, 0, count - 1)
        for proxy in proxies:
            yield proxy.decode("utf-8")

    def count_all_proxies(self):
        """
        返回所有代理总数
        """
        return self.redis.zcard(REDIS_KEY)

    def count_score_proxies(self, score):
        """
        返回指定分数代理总数

        :param score: 代理分数
        """
        if 0 <= score <= 10:
            proxies = self.redis.zrangebyscore(REDIS_KEY, score, score)
            return len(proxies)
        return -1

    def clear_proxies(self, score):
        """
        删除分数小于等于 score 的代理
        """
        if 0 <= score <= 10:
            proxies = self.redis.zrangebyscore(REDIS_KEY, 0, score)
            for proxy in proxies:
                self.redis.zrem(REDIS_KEY, proxy)
            return True
        return False

    def all_proxies(self):
        """
        返回全部代理
        """
        return self.redis.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)
