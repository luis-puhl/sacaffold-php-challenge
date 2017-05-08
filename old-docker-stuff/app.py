from flask import Flask
from redis import Redis, RedisError
import os
import socket

import time

# Connect to Redis
redis = Redis(host="redis", db=0)

app = Flask(__name__)

@app.route("/")
def hello():
    try:
        visits = redis.incr('counter')
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

	# while True: range(10000) and None; time.sleep(0.2)      # 1% CPU
	while True: range(10000) and None; time.sleep(0.02)     # 15% CPU
	# while True: range(10000) and None; time.sleep(0.002)    # 60% CPU
	# while True: range(10000) and None; time.sleep(0.0002)   # 86% CPU

    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Visits:</b> {visits}"
    return html.format(name=os.getenv('NAME', "world"), hostname=socket.gethostname(), visits=visits)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80)
