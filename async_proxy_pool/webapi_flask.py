#!/usr/bin/env python
# coding=utf-8

from flask import Flask, jsonify
from async_proxy_pool.database import RedisClient

app = Flask(__name__)
redis_conn = RedisClient()


@app.route("/")
def index():
    return jsonify({"Welcome": "This is a proxy pool system."})


@app.route("/pop")
def pop_proxy():
    proxy = redis_conn.pop_proxy().decode("utf8")
    if proxy[:5] == "https":
        return jsonify({"https": proxy})
    else:
        return jsonify({"http": proxy})


@app.route("/get/<int:count>")
def get_proxy(count):
    res = []
    for proxy in redis_conn.get_proxies(count):
        if proxy[:5] == "https":
            res.append({"https": proxy})
        else:
            res.append({"http": proxy})
    return jsonify(res)


@app.route("/count")
def count_all_proxies():
    count = redis_conn.count_all_proxies()
    return jsonify({"count": str(count)})


@app.route("/count/<int:score>")
def count_score_proxies(score):
    count = redis_conn.count_score_proxies(score)
    return jsonify({"count": str(count)})


@app.route("/clear/<int:score>")
def clear_proxies(score):
    if redis_conn.clear_proxies(score):
        return jsonify({"Clear": "Successful"})
    return jsonify({"Clear": "Score should >= 0 and <= 10"})
